# system_context.py
import os
import psutil
from ai_assistant.utils import log_action

def get_system_context():
    context = {
        "open_files": [],
        "running_apps": [],
        "drives": []
    }

    # Get files from C:\ and U:\
    for drive in ["C:\\", "U:\\"]:
        try:
            files = os.listdir(drive)
            context["open_files"].extend([os.path.join(drive, f) for f in files if os.path.isfile(os.path.join(drive, f))])
            context["drives"].append(drive)
        except Exception as e:
            log_action(f"[⚠️] Error reading {drive}: {e}")

    # Get running apps
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            context["running_apps"].append(proc.info['name'])
        except Exception as e:
            log_action(f"[⚠️] Error getting process info: {e}")

    return context

def format_context_for_prompt(context):
    lines = []

    if context["open_files"]:
        lines.append("Files in main drives:")
        for f in context["open_files"][:10]:
            lines.append(f"• {f}")

    if context["running_apps"]:
        lines.append("\nRunning applications:")
        for app in context["running_apps"][:10]:
            lines.append(f"• {app}")

    return "\n".join(lines)
