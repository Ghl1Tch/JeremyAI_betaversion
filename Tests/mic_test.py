import sounddevice as sd
import numpy as np

device = 1

print("Say anything for 5 seconds...")

recording = sd.rec(
    int(5 * 16000),
    samplerate=16000,
    channels=1,
    device=device
)

sd.wait()

volume = np.max(np.abs(recording))

print("Volume:", volume)

if volume > 0.01:
    print("Mic worked")
else:
    print("Mic not worked")

#This test for mic