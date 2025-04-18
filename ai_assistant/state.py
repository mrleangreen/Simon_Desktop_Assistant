# state.py

cancel_task = False
manual_override = False

def set_cancel_task(val):
    global cancel_task
    cancel_task = val

def get_cancel_task():
    return cancel_task

def set_manual_override(val):
    global manual_override
    manual_override = val

def get_manual_override():
    return manual_override
