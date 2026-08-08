import subprocess
from pathlib import Path


class Speaker:
    def __init__(self, settings):
        self.executable = Path(
            settings["piper_executable"]
        )

        self.model = Path(
            settings["piper_model"]
        )

        self.config = Path(
            settings["piper_config"]
        )

        self.output = (
            self.executable.parent
            / "jeremy_output.wav"
        )

    def say(self, text):
        if not self.executable.exists():
            print(
                f"Piper not found: {self.executable}"
            )
            return

        if not self.model.exists():
            print(
                f"Piper voice not found: {self.model}"
            )
            return

        command = [
            str(self.executable),
            "--model",
            str(self.model),
            "--output_file",
            str(self.output),
        ]

        if self.config.exists():
            command.extend(
                [
                    "--config",
                    str(self.config),
                ]
            )

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

        # Play the generated voice on Windows.
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