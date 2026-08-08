from core.brain import Brain
from core.config_loader import load_settings
from core.memory import Memory

from voice.listener import Listener
from voice.speaker import Speaker
from voice.whisper import WhisperTranscriber


def main():
    settings = load_settings()

    memory = Memory(settings["memory_file"])
    brain = Brain(settings, memory)

    listener = Listener(settings)
    transcriber = WhisperTranscriber(settings)
    speaker = Speaker(settings)

    print("Jeremy AI Beta 1.0")
    print("Running in background. Say 'Jeremy' to wake him.")
    print("Press Ctrl+C to stop.\n")

    try:
        while True:
            audio_file = listener.wait_for_speech()

            if not audio_file:
                continue

            text = transcriber.transcribe(audio_file)

            if not text:
                continue

            print(f"You: {text}")

            if not brain.is_wake_command(text):
                continue

            command = brain.remove_wake_command(text)

            if not command:
                speaker.say("Yes?")
                continue

            answer = brain.ask(command)

            print(f"Jeremy: {answer}")
            speaker.say(answer)

    except KeyboardInterrupt:
        print("\nJeremy stopped.")


if __name__ == "__main__":
    main()