import torch
from silero_vad import load_silero_vad


class SileroVAD:
    def __init__(self, threshold=0.5):
        self.threshold = threshold

        # Load the Silero model once when Jeremy starts.
        self.model = load_silero_vad()

        self.sample_rate = 16000
        self.chunk_size = 512

    def is_speech(self, audio):
        """
        Check whether the current audio chunk contains speech.

        Silero VAD expects 512 samples at 16 kHz,
        so longer audio is split into smaller chunks.
        """

        if len(audio) == 0:
            return False

        audio_tensor = torch.from_numpy(audio).float()

        if audio_tensor.dim() > 1:
            audio_tensor = audio_tensor.squeeze()

        # Split the audio into chunks Silero can process.
        chunks = torch.split(audio_tensor, self.chunk_size)

        probabilities = []

        for chunk in chunks:
            # Ignore the last incomplete chunk.
            if chunk.shape[-1] != self.chunk_size:
                continue

            probability = self.model(
                chunk,
                self.sample_rate,
            )

            probabilities.append(float(probability))

        if not probabilities:
            return False

        # If any part of the audio contains speech,
        # consider the whole audio chunk as speech.
        return max(probabilities) >= self.threshold