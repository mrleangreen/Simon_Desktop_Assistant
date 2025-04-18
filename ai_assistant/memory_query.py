# memory_query.py
from ai_assistant.memory import search_memory
from ai_assistant.utils import log_action

def query_memory():
    query = input("Search your memory for what?\n> ").strip()
    if not query:
        print("[!] No query entered.")
        return

    results = search_memory(query)
    if not results:
        print("[📭] No memory found matching that.")
        return

    print(f"[📚] {len(results)} memory entries found:\n")
    for entry in results:
        print(f"🕒 {entry['timestamp']}")
        print(f"📝 Prompt: {entry['prompt']}")
        print("🧩 Actions:")
        for a in entry['actions']:
            print(f"   → {a}")
        print("\n" + "-"*50 + "\n")
