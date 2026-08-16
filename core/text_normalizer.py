class TextNormalizer:
    def __init__(self):
        self.wake_word_replacements = {
            "джеремия": "джереми",
            "джеремий": "джереми",
            "джеремие": "джереми",
            "джеремию": "джереми",
            "джеремии": "джереми",
            "джеремень" : "джереми",
            "джейреми" : "джереми",
            "джейлеми" : "джереми",
            "джерими" : "джереми",
            "джейрими" : "джереми",
            "джерри" : "джереми",
            "джейлими" : "джереми",
            "джей" : "джереми",
            "джейдеми" : "джереми",
            "джерями" : "джереми",
            "джеллими" : "джереми",
            "джйдеми" : "джереми",
            "джеремень" : "джереми"
            
        }

        self.application_replacements = {
            "дис корд": "дискорд",
            "дискорд": "дискорд",
            "вэскаде": "vs code",
            "в эскаде": "vs code",
            "эскаде": "vs code",
        }

        self.common_replacements = {
            "ютюб": "youtube",
            "ю туб": "youtube",
        }

    def normalize(self, text):
        text = text.lower().strip()

        for wrong, correct in self.wake_word_replacements.items():
            text = text.replace(wrong, correct)

        for wrong, correct in self.application_replacements.items():
            text = text.replace(wrong, correct)

        for wrong, correct in self.common_replacements.items():
            text = text.replace(wrong, correct)

        return text