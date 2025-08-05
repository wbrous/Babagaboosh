from RealtimeSTT import AudioToTextRecorder
from rich import print

class SpeechToText:
    def __init__(self):
        self.recorder = AudioToTextRecorder(
            spinner=False,
            model="base",  # Use base model for better accuracy
            language="en",
            silero_sensitivity=0.6,  # Higher sensitivity
            webrtc_sensitivity=2,  # Lower value = more sensitive
            post_speech_silence_duration=1.0,  # Wait longer for complete speech
            min_length_of_recording=1.0,  # Minimum 1 second of audio
            min_gap_between_recordings=0,
            enable_realtime_transcription=False,  # Disable for process_once
            use_microphone=True,
            on_recording_start=lambda: print("[yellow]🎤 Recording started...[/yellow]"),
            on_recording_stop=lambda: print("[yellow]⏹️ Recording stopped, processing...[/yellow]")
        )

    def process_once(self):
        """Process a single text input and return the transcribed text."""
        print("[yellow]Listening... Speak now![/yellow]")

        # Use a list to capture the text from the callback
        captured_text = []
        
        def capture_text(text):
            if text.strip():  # Only capture non-empty text
                captured_text.append(text.strip())
        
        # Record and transcribe
        self.recorder.text(capture_text)
        
        # Return the captured text or None if nothing was captured
        return captured_text[0] if captured_text else None
    
    def shutdown(self):
        """Properly shutdown the recorder."""
        if hasattr(self.recorder, 'shutdown'):
            self.recorder.shutdown()