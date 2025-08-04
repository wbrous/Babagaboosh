from RealtimeSTT import AudioToTextRecorder

class SpeechToText:
    def __init__(self, start_key='F4'):
        self.recorder = AudioToTextRecorder(
            spinner=False,
            model="tiny",
            language="en",
            silero_sensitivity=0.4,
            webrtc_sensitivity=3,
            post_speech_silence_duration=0.7,
            min_length_of_recording=0,
            min_gap_between_recordings=0,
            enable_realtime_transcription=True,
            realtime_processing_pause=0.2,
            realtime_model_type='tiny.en',
            use_microphone=True
        )

    def process_once(self):
        """Process a single text input."""
        return self.recorder.text(lambda text: text)