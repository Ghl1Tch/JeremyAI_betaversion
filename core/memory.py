import json
from pathlib import Path


class Memory:
    def __init__(self, file_path):
        self.file_path = Path(file_path)
        self.file_path.parent.mkdir(parents=True, exist_ok=True)

        if self.file_path.exists():
            try:
                self.data = json.loads(
                    self.file_path.read_text(
                        encoding="utf-8"
                    )
                )
            except (json.JSONDecodeError, OSError):
                self.data = {"facts": []}
        else:
            self.data = {"facts": []}
            self._save()

    def add_fact(self, fact):
        if fact not in self.data["facts"]:
            self.data["facts"].append(fact)
            self._save()

    def get_facts(self):
        return self.data.get("facts", [])

    def _save(self):
        self.file_path.write_text(
            json.dumps(
                self.data,
                ensure_ascii=False,
                indent=4,
            ),
            encoding="utf-8",
        )