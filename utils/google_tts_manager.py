from gtts import gTTS
import tempfile

class GoogleTTSManager:
    def __init__(self, language='en'):
        self.language = language

    def text_to_speech(self, text, filename=None):
        tts = gTTS(text=text, lang=self.language)
        if filename is None:
            with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                temp_filename = tmp_file.name
                tts.save(temp_filename)
            return temp_filename
        else:
            tts.save(filename)
            return filename