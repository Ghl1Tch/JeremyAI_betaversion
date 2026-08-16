import time
import wave
from pathlib import Path

import numpy as np
import sounddevice as sd

from voice.vad import SileroVAD


class Listener:
    def __init__(self, settings):
        self.sample_rate = settings["sample_rate"]
        self.channels = settings["channels"]

        self.silence_duration = settings["silence_duration"]
        self.max_record_seconds = settings["max_record_seconds"]

        self.root = Path(settings["_project_root"])

        self.vad = SileroVAD(
            threshold=settings["vad_threshold"]
        )

    def wait_for_speech(self, timeout=None):
        print("Listening...")

        chunk_time = 0.1
        chunk_size = int(
            self.sample_rate * chunk_time
        )

        chunks = []

        speaking = False
        silence = 0.0

        started = time.monotonic()
        wait_started = time.monotonic()

        with sd.InputStream(
            samplerate=self.sample_rate,
            channels=self.channels,
            dtype="float32",
            blocksize=chunk_size,
        ) as stream:

            while True:
                data, _ = stream.read(chunk_size)

                audio = data[:, 0].copy()

                speech = self.vad.is_speech(audio)

                if speech:
                    speaking = True
                    silence = 0.0

                    chunks.append(audio)

                elif speaking:
                    # Keep recording during short pauses.
                    chunks.append(audio)

                    silence += chunk_time

                    if silence >= self.silence_duration:
                        break

                if (
                    timeout is not None
                    and not speaking
                    and time.monotonic() - wait_started >= timeout
                ):
                    break

                if (
                    time.monotonic() - started
                    >= self.max_record_seconds
                ):
                    break

        if not speaking or not chunks:
            return None

        audio = np.concatenate(chunks)

        output = self.root / "temp_audio.wav"

        pcm = np.clip(
            audio * 32767,
            -32768,
            32767,
        ).astype(np.int16)

        with wave.open(str(output), "wb") as wav:
            wav.setnchannels(1)
            wav.setsampwidth(2)
            wav.setframerate(self.sample_rate)
            wav.writeframes(pcm.tobytes())

        return str(output)