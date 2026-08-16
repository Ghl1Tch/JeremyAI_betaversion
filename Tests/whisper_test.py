from faster_whisper import WhisperModel
import sounddevice as sd
import numpy  as np
device = 1
print("Downloading Whisper...")
model = WhisperModel(
    "small",
    device="cpu",
    compute_type="int8"
)
print("Say anything for 5 seconds...")
audio = sd.rec(
    int(5*16000),
    samplerate=16000,
    channels=1,
    device=device
)
sd.wait()
audio = audio.flatten().astype(np.float32)
segments, info = model.transcribe(
    audio,
    language="ru"
)
print("You said:")
for segment in segments:
    print(segment.text)
#Test for Whisper