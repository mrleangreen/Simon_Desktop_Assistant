import os
from ai_assistant.ai_interface import ask_mistral
from ai_assistant.utils import log_action

BASE_DIR = os.path.abspath("generated_projects")

def generate_project(prompt, folder_name="autogen_project"):
    project_path = os.path.join(BASE_DIR, folder_name)
    os.makedirs(project_path, exist_ok=True)
    log_action(f"[⚙️] Generating: '{prompt}' → {project_path}")
    user_prompt = f"""You are an expert software engineer.
Generate a complete coding project based on the following description:

"{prompt}"

Use clear filenames and realistic code inside markdown-style code blocks.
Example:

/main.py
```python
# code here
```
Include all necessary files. Don't explain anything.
"""
    code_output = ask_mistral(user_prompt)
    parse_and_write_files(code_output, project_path)
    log_action("[✅] Project generated successfully.")
    return project_path

def parse_and_write_files(response_text, root):
    current_file = None
    content_lines = []
    recording = False
    for line in response_text.splitlines():
        if line.startswith("/") and "." in line:
            current_file = line.strip("/")
        elif line.startswith("```") and recording:
            if current_file and content_lines:
                write_file(root, current_file, content_lines)
            content_lines = []
            recording = False
        elif line.startswith("```") and not recording:
            recording = True
        elif recording and current_file:
            content_lines.append(line)

def write_file(base, filename, lines):
    full_path = os.path.join(base, filename)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    log_action(f"[📁] Wrote: {filename}")
