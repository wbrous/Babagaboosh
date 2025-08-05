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

class AIChatApp:
    def __init__(self):
        self.speech_to_text = SpeechToText(config['stt']['model'], config['stt']['language'])
        self.audio_manager = AudioManager()
        self.google_tts_manager = GoogleTTSManager(language=config['tts']['language'])
        self.polly_tts_manager = PollyTTSManager(
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            region_name=config['tts']['region']
        )
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
                    print(f"\n[blue]AI Response: {response}[/blue]")
                    try:
                        file_path = self.polly_tts_manager.text_to_speech(response, "response.mp3", True, config['tts']['voice'], 'mp3')
                    except Exception as e:
                        print(f"[red]Error with Polly TTS: {e}[/red]")
                        print("[yellow]Falling back to Google TTS...[/yellow]")
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

def setup_obs():
    """Setup OBS WebSocket connection if enabled."""

    if os.getenv('USE_OBS_WEBSOCKET', '0') == '1':
        from obswebsocket import obsws, requests
        obs = None  # Global OBS instance
        try:
            obs = obsws(
                host=os.getenv('OBS_WEBSOCKET_HOST', 'localhost'),
                port=int(os.getenv('OBS_WEBSOCKET_PORT', 4455)),
                password=os.getenv('OBS_WEBSOCKET_PASSWORD', '') if os.getenv('USE_OBS_WEBSOCKET_PASSWORD', '0') == '1' else ''
            )
            obs.connect()
            print("[green]Connected to OBS WebSocket successfully[/green]")
        except Exception as e:
            print(f"[red]Error connecting to OBS WebSocket: {e}[/red]")
            obs = None
    else:
        obs = None  # OBS not used

    return obs

def load_config():
    """Load configuration from YAML file."""
    yaml_config_path = os.path.join(os.path.dirname(__file__), 'config.yaml')
    if not os.path.exists(yaml_config_path):
        print(f"Config file not found at {yaml_config_path}. Please ensure it exists.")
        sys.exit(1)

    with open(yaml_config_path, 'r') as file:
        config = yaml.load(file, Loader=yaml.FullLoader)

    return config

if __name__ == '__main__':
    config = load_config()
    obs = setup_obs()
    app = AIChatApp()
    print("[green]AI Chat App initialized successfully.[/green]")
    app.begin_conversation()