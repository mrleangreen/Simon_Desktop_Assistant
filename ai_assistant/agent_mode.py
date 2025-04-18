# agent_mode.py
from ai_assistant.ai_interface import ask_mistral
from ai_assistant.task_planner import plan_and_execute
from ai_assistant.codegen_agent import generate_project
from ai_assistant.actions import run_action
from ai_assistant.utils import log_action

def agent_mode(prompt):
    log_action(f"[🧠🤖] Agent Mode activated: {prompt}")

    clarify_prompt = f"""
You are a goal-oriented assistant. A user has given you this goal:

"{prompt}"

Your job is to:
1. Determine if this task is simple, multi-step, or requires generating code
2. If the task is vague or needs clarification, return a question to ask the user
3. If it's ready, reply with one of the following tags only:
- RUN_ACTION: followed by a single-step command (e.g., RUN_ACTION: open chrome)
- PLAN: followed by a sentence to break into multiple steps
- CODEGEN: followed by a prompt for a code project

Only reply with one of those options.
"""

    response = ask_mistral(clarify_prompt).strip()

    if response.startswith("RUN_ACTION:"):
        command = response.replace("RUN_ACTION:", "").strip()
        log_action(f"[🤖] Agent chose run_action: {command}")
        run_action(command)

    elif response.startswith("PLAN:"):
        plan_task = response.replace("PLAN:", "").strip()
        log_action(f"[🧩] Agent chose plan_and_execute: {plan_task}")
        plan_and_execute(plan_task)

    elif response.startswith("CODEGEN:"):
        code_task = response.replace("CODEGEN:", "").strip()
        log_action(f"[🛠] Agent chose generate_project: {code_task}")
        generate_project(code_task)

    else:
        log_action(f"[❓] Agent needs clarification: {response}")
        answer = input(f"[AI Assistant asks] {response}\n> ")
        agent_mode(answer)
