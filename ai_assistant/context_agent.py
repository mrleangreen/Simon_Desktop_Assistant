# context_agent.py
from ai_assistant.system_context import get_system_context, format_context_for_prompt
from ai_assistant.ai_interface import ask_mistral
from ai_assistant.utils import log_action
from ai_assistant.actions import run_action

def decide_and_execute(user_goal):
    context = get_system_context()
    context_text = format_context_for_prompt(context)

    full_prompt = f"""
You are a smart assistant with access to the user's file system, open applications, and running processes.

Here is the current system context:
{context_text}

Based on this context, how would you complete the following user request?
Only respond with one simple actionable command. No explanations.

User goal: {user_goal}
"""

    action = ask_mistral(full_prompt).strip()
    log_action(f"[🎯 AI Decision] {action}")
    run_action(action)
    return action
