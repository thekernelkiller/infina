from typing import List, Dict, Union

class SessionMemory:
    def __init__(self):
        self.history: List[Dict[str, str]] = []

    def add_message(self, role: str, content: str):
        if role not in ["user", "bot"]:
            raise ValueError("Role must be 'user' or 'bot'.")
        self.history.append({"role": role, "content": content})

    def get_history(self) -> List[Dict[str, str]]:
        return self.history

    def get_formatted_history(self, max_turns: int = 0) -> List[str]:
        formatted = [f"{msg['role'].capitalize()}: {msg['content']}" for msg in self.history]
        if max_turns > 0 and len(formatted) > max_turns:
            return formatted[-max_turns:]
        return formatted

    def clear(self):
        self.history = []

if __name__ == '__main__':
    memory = SessionMemory()
    memory.add_message("user", "Hello there!")
    memory.add_message("bot", "Hi! How can I help you?")
    memory.add_message("user", "Tell me about adaptive AI.")

    print("Full History (raw):")
    print(memory.get_history())

    print("\nFormatted History (all turns):")
    for line in memory.get_formatted_history():
        print(line)

    print("\nFormatted History (last 2 turns):")
    for line in memory.get_formatted_history(max_turns=2):
        print(line)

    memory.clear()
    print("\nHistory after clearing:")
    print(memory.get_history()) 