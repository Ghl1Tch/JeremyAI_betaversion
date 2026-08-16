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
            vad_parameters={"min_silence_duration_ms": 500},
            beam_size=5,
            condition_on_previous_text=True,#context
            temperature=0,
            no_speech_threshold=0.6
        )

        return " ".join(
            segment.text.strip()
            for segment in segments
        ).strip()