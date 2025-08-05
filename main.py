import os
import sys
import time
import yaml
import dotenv
import keyboard
from utils import *

from rich import print

dotenv.load_dotenv(
    dotenv_path=os.path.join(os.path.dirname(__file__), '.env'),
    override=True
)

yaml_config_path = os.path.join(os.path.dirname(__file__), 'config.yaml')
if not os.path.exists(yaml_config_path):
    print(f"Config file not found at {yaml_config_path}. Please ensure it exists.")
    sys.exit(1)

with open(yaml_config_path, 'r') as file:
    config = yaml.load(file, Loader=yaml.FullLoader)

class AIChatApp:
    def __init__(self):
        self.speech_to_text = SpeechToText(config['stt']['model'], config['stt']['language'])
        self.audio_manager = AudioManager()
        self.google_tts_manager = GoogleTTSManager(language=config['tts']['language'])
        self.gemini_ai_manager = GeminiAIManager(
            api_key=os.getenv("GEMINI_API_KEY"),
            model=config['ai']['model'],
            system_instruction=config['ai']['system_instruction']
        )
    
    def begin_conversation(self):
        print("Starting conversation with AI...")
        try:
            while True:
                print("\n[green]Press F4 to start recording...[/green]")
                keyboard.wait('f4')  # wait for F4 key press
                print("[green]--- Ready for input ---[/green]")
                user_input = self.speech_to_text.process_once()
                
                if user_input:
                    print(f"\n[blue]You said: {user_input}[/blue]\n")
                    response = self.gemini_ai_manager.generate_response(user_input)
                    print(f"\n[yellow]AI Response: {response}[/yellow]")

                    file_path = self.google_tts_manager.text_to_speech(response, "response.mp3")
                    self.audio_manager.load_audio(file_path)
                    self.audio_manager.play_audio(file_path)
                    time.sleep(self.audio_manager.get_audio_length(file_path))
                    print("[green]AI response played back.[/green]")
                    self.audio_manager.unload_audio(file_path)
                else:
                    print("[red]No clear speech detected. Please try speaking again...[/red]")

        except KeyboardInterrupt:
            print("\nShutting down...")
            self.speech_to_text.shutdown()
        except Exception as e:
            print(f"[red]Error: {e}[/red]")
            self.speech_to_text.shutdown()

if __name__ == '__main__':
    app = AIChatApp()
    print("[green]AI Chat App initialized successfully.[/green]")
    app.begin_conversation()