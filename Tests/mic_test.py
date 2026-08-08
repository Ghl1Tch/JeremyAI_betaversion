import sounddevice as sd
import numpy as np

device = 1

print("Говори что-нибудь 5 секунд...")

recording = sd.rec(
    int(5 * 16000),
    samplerate=16000,
    channels=1,
    device=device
)

sd.wait()

volume = np.max(np.abs(recording))

print("Громкость:", volume)

if volume > 0.01:
    print("Микрофон работает")
else:
    print("Микрофон не работает")
    
