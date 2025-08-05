from gtts import gTTS
import tempfile
import os

class GoogleTTSManager:
    def __init__(self, language='en'):
        self.language = language

    def text_to_speech(self, text, filename=None):
        """Convert text to speech using Google TTS and save to a file."""
        tts = gTTS(text=text, lang=self.language)

        if filename is None:
            fd, filename = tempfile.mkstemp(dir=os.path.join(os.path.dirname(__file__), '..', 'audio'), prefix='google_', suffix='.mp3')
            os.close(fd)
        
        tts.save(filename)
        return filename