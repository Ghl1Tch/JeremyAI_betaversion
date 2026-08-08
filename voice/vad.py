import torch
from silero_vad import load_silero_vad


class SileroVAD:
    def __init__(self, threshold=0.5):
        self.threshold = threshold

        # Load the Silero model once when Jeremy starts.
        self.model = load_silero_vad()

        self.sample_rate = 16000

    def is_speech(self, audio):
        """
        Check whether the current audio chunk contains speech.

        Silero expects a torch tensor with 16 kHz audio.
        """

        if len(audio) == 0:
            return False

        audio_tensor = torch.from_numpy(audio)

        if audio_tensor.dim() > 1:
            audio_tensor = audio_tensor.squeeze()

        probability = self.model(
            audio_tensor,
            self.sample_rate,
        )

        return float(probability) >= self.threshold