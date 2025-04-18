# task_planner.py
import json
from ai_assistant.ai_interface import ask_mistral
from ai_assistant.utils import log_action
from ai_assistant.actions import run_action
from ai_assistant.memory import remember_task


def plan_and_execute(prompt):
    log_action(f"[🧠] Planning task: {prompt}")

    planning_prompt = f"""
You are a task planner assistant.
Break down the following goal into a list of executable desktop-level commands.
Each step must be atomic and match the capabilities of a desktop assistant:
- open apps
- type text
- click on elements
- generate code or files
- move or organize files

Respond with one step per line, no numbers or bullets.
Avoid explanations.

Goal: {prompt}
"""

    steps_raw = ask_mistral(planning_prompt)
    steps = [s.strip() for s in steps_raw.strip().splitlines() if s.strip()]

    log_action("[📋] Task plan:")
    for step in steps:
        log_action(f" → {step}")

    for step in steps:
        if step:
            confirmed = True  # future: add confirm_gui(step)
            if confirmed:
                run_action(step)
            else:
                log_action(f"[-] Skipped step: {step}")

    remember_task(prompt, steps)
    log_action("[✅] Multi-step task completed.")