from faster_whisper import WhisperModel


class WhisperTranscriber:
    def __init__(self, settings):
        self.language = settings["whisper_language"]

        self.model = WhisperModel(
            settings["whisper_model"],
            device="cpu",
            compute_type="int8",
        )

    def transcribe(self, audio_file):
        segments, _ = self.model.transcribe(
            audio_file,
            language=self.language,
            vad_filter=True,
        )

        return " ".join(
            segment.text.strip()
            for segment in segments
        ).strip()