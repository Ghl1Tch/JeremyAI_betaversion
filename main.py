import time
from core.brain import Brain
from core.config_loader import load_settings
from core.memory import Memory
from core.text_normalizer import TextNormalizer
from voice.listener import Listener
from voice.speaker import Speaker
from voice.whisper import WhisperTranscriber


def main():
    settings = load_settings()

    memory = Memory(settings["memory_file"])
    brain = Brain(settings, memory)

    listener = Listener(settings)
    transcriber = WhisperTranscriber(settings)
    normalizer = TextNormalizer()
    speaker = Speaker(settings)

    active = False
    active_timeout = 5

    print("Jeremy AI Beta 1.0")
    print("Running in background. Say 'Jeremy' to wake him.")
    print("Press Ctrl+C to stop.\n")

    try:
        while True:
            if active:
                audio_file = listener.wait_for_speech(
                    timeout=active_timeout
                )
            else:
                audio_file = listener.wait_for_speech()

            if not audio_file:
                if active:
                    active = False
                    print("Jeremy is no longer active.\n")

                continue

            text = transcriber.transcribe(audio_file)

            if not text:
                continue

            text = normalizer.normalize(text)

            print(f"You: {text}")

            if not active:
                if not brain.is_wake_command(text):
                    continue

                active = True

                command = brain.remove_wake_command(text)

                if not command:
                    speaker.say("Yes?")
                    continue

            else:
                command = text

            if not command:
                continue

            answer = brain.ask(command)

            print(f"Jeremy: {answer}")
            speaker.say(answer)

            active = True

            print("Jeremy is active for 5 seconds.\n")

    except KeyboardInterrupt:
        print("\nJeremy stopped.")


if __name__ == "__main__":
    main()