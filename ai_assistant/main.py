from ai_assistant.ui import confirm_gui, create_tray_icon
from ai_assistant.actions import run_action
from ai_assistant.listeners import start_listeners
from ai_assistant.ai_interface import ask_mistral
from ai_assistant.codegen_agent import generate_project
from ai_assistant.task_planner import plan_and_execute
from ai_assistant.utils import log_action
from ai_assistant.window_control import list_open_windows, activate_window_by_title, close_window_by_title
from ai_assistant.ai_vision import click_on_image
from ai_assistant.memory import search_memory, load_memory
from ai_assistant.memory_query import query_memory
import re

def enrich_prompt(user_input):
    memory_hits = search_memory(user_input)
    if memory_hits:
        context = "\n".join(
            f"Task: {m['prompt']}\nActions: {', '.join(m['actions'])}"
            for m in memory_hits[:3]
        )
        return f"Here is what you've done in the past:\n{context}\n\nNow do this:\n{user_input}"
    return user_input

def suggest_next_task(latest_prompt):
    memory = load_memory()
    for entry in reversed(memory):
        if entry["prompt"] != latest_prompt and any(word in latest_prompt.lower() for word in entry["prompt"].lower().split()):
            return entry["prompt"]
    return None

def main():
    create_tray_icon()
    print("\U0001F9E0 Local AI Assistant is ready. Press ESC or right-click to cancel any task.")

    while True:
        user_input = input("\nWhat should I do? (or type 'exit')\n> ")
        if user_input.strip().lower() == "exit":
            break

        if user_input.strip().lower().startswith("memory search"):
            query_memory()
            continue

        if any(word in user_input.lower() for word in ["generate", "build", "create a website", "make a flask app", "write an api", "assignment", "homework"]):
            log_action(f"[🛠] Codegen or assignment detected: {user_input}")
            plan_and_execute(user_input)
            continue

        if any(keyword in user_input.lower() for keyword in [
            "create table", "sql schema", "foreign key", "insert into", "sample data", "database project"
        ]):
            log_action(f"[🛠] Detected SQL/DB project: {user_input}")
            generate_project(user_input)
            continue

        if any(word in user_input.lower() for word in ["and then", "multiple things", "step by step", "do all this"]):
            log_action(f"[🤖] Multi-step task detected.")
            plan_and_execute(user_input)
            continue

        enriched_prompt = enrich_prompt(user_input)
        ai_reply = ask_mistral(
            f"""
You are an advanced autonomous Windows desktop agent.

Your role is to interpret the user's instruction and respond with exactly one atomic command that you can execute via mouse, keyboard, file, or system operations. Keep your output short, raw, and functional.

Only respond with one actionable command like:
- open chrome
- move mouse
- click search bar
- type "hello world"
- open notepad
- read screen
- build flask app with login and MongoDB
- close window titled "Spotify"

Rules:
- DO NOT explain or describe anything
- DO NOT use code formatting or markdown
- DO NOT wrap commands in quotes (unless it's a string input like typing text)
- Your response MUST be executable as a single command

User instruction: {enriched_prompt}
"""
        )

        task = ai_reply.strip()
        log_action(f"[AI \U0001F4AC] {task}")

        if not confirm_gui(task):
            log_action("[-] Task rejected.")
            continue

        esc_thread, click_thread = start_listeners()

        # ✅ Multi-step command parsing with &&, &, then, and then
        task_normalized = re.sub(r"\b(and then|then|next)\b", "&&", task, flags=re.IGNORECASE)
        task_normalized = task_normalized.replace("&", "&&")
        steps = [s.strip() for s in task_normalized.split("&&") if s.strip()]
        for step in steps:
            run_action(step)

        esc_thread.join()
        click_thread.join()

        suggested = suggest_next_task(user_input)
        if suggested:
            cont = input(f"💡 Based on your history, want to also: {suggested}? (y/n) ").strip().lower()
            if cont == "y":
                plan_and_execute(suggested)

        cont = input("Give AI another task? (y/n): ").strip().lower()
        if cont != "y":
            break

if __name__ == "__main__":
    main()


