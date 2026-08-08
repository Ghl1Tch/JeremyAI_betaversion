import re

import requests


SYSTEM_PROMPT = """
You are Jeremy, a personal desktop AI assistant.

Be natural, helpful and concise.
Talk like a normal assistant, not like a textbook.

Always answer in the user's language unless asked otherwise.

You are running as a desktop assistant in the background.
"""


class Brain:
    def __init__(self, settings, memory):
        self.settings = settings
        self.memory = memory
        self.history = []

    def is_wake_command(self, text):
        text = text.lower()

        return any(
            word.lower() in text
            for word in self.settings["wake_words"]
        )

    def remove_wake_command(self, text):
        result = text

        for word in self.settings["wake_words"]:
            result = re.sub(
                rf"\b{re.escape(word)}\b[:,]?\s*",
                "",
                result,
                flags=re.IGNORECASE,
            )

        return result.strip()

    def ask(self, text):
        facts = self.memory.get_facts()

        memory_text = "\n".join(facts[-20:])

        if not memory_text:
            memory_text = "(none)"

        messages = [
            {
                "role": "system",
                "content": (
                    SYSTEM_PROMPT
                    + "\n\nKnown memory:\n"
                    + memory_text
                ),
            }
        ]

        messages.extend(self.history[-10:])

        messages.append(
            {
                "role": "user",
                "content": text,
            }
        )

        response = requests.post(
            self.settings["ollama_url"],
            json={
                "model": self.settings["ollama_model"],
                "messages": messages,
                "stream": False,
            },
            timeout=120,
        )

        response.raise_for_status()

        answer = response.json()["message"]["content"].strip()

        self.history.append(
            {
                "role": "user",
                "content": text,
            }
        )

        self.history.append(
            {
                "role": "assistant",
                "content": answer,
            }
        )

        return answer