import subprocess
import sys
from pathlib import Path
class Speaker:
    def __init__(self, settings):
        self.model = Path(settings["piper_model"])
        self.config = Path(settings["piper_config"])
        self.output = (
            self.model.parent / "jeremy_output.wav"
        )
    def say(self, text):
        if not self.model.exists():
            print(f"Piper voice not found: {self.model}")
            return
        command = [
            sys.executable,
            "-m",
            "piper",
            "-m",
            str(self.model),
            "-f",
            str(self.output),
        ]
        if self.config.exists():
            command.extend([
                "-c",
                str(self.config),
            ])
        result = subprocess.run(
            command,
            input=text,
            text=True,
            capture_output=True,
        )
        if result.returncode != 0:
            print("Piper error:")
            print(result.stderr)
            return
        subprocess.run(
            [
                "powershell",
                "-NoProfile",
                "-Command",
                (
                    f'(New-Object Media.SoundPlayer '
                    f'"{self.output}").PlaySync()'
                ),
            ],
            capture_output=True,
            text=True,
        )