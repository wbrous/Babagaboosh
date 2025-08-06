import os
import sys
import time
import yaml
import dotenv
import keyboard
from managers import *

from rich import print

dotenv.load_dotenv(
    dotenv_path=os.path.join(os.path.dirname(__file__), '.env'),
    override=True
)

class AIChatApp:
    def __init__(self):
        """Initialize the AI Chat Application."""
        print("[yellow]Initializing AI Chat App...[/yellow]")
        self.config = load_config()
        self.audio_manager = AudioManager()
        self.google_tts_manager = GoogleTTSManager(language=self.config['tts']['language'])
        self.speech_to_text = SpeechToText(self.config['stt']['model'], self.config['stt']['language'])
        self.obs_enabled = self.config['obs']['enabled']
        if self.obs_enabled:
            # Determine password only once, not via lambda
            obs_password = os.getenv("OBS_WEBSOCKET_PASSWORD") if os.getenv("USE_OBS_WEBSOCKET_PASSWORD", "0") == "1" else None
            self.obs_websockets_manager = OBSWebsocketsManager(
                host=os.getenv("OBS_WEBSOCKET_URL"),
                port=int(os.getenv("OBS_WEBSOCKET_PORT", 4455)),
                password=obs_password
            )
        else:
            print("[yellow]OBS WebSocket is disabled in the self.configuration.[/yellow]")
        self.polly_tts_manager = PollyTTSManager(
            aws_access_key_id=os.getenv("AMAZON_POLLY_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AMAZON_POLLY_SECRET_ACCESS_KEY"),
            region_name=self.config['tts']['region'],
            engine=self.config['tts']['engine']
        )
        self.gemini_ai_manager = GeminiAIManager(
            api_key=os.getenv("GEMINI_API_KEY"),
            model=self.config['ai']['model'],
            system_instruction=self.config['ai']['system_instruction']
        )

        print("[green]AI Chat App initialized successfully.[/green]")

        self.audio_manager.load_audio(os.path.join(os.path.dirname(__file__), 'start.mp3'))
        self.audio_manager.play_audio(os.path.join(os.path.dirname(__file__), 'start.mp3'))
        time.sleep(self.audio_manager.get_audio_length(os.path.join(os.path.dirname(__file__), 'start.mp3')))
        self.audio_manager.unload_audio(os.path.join(os.path.dirname(__file__), 'start.mp3'), remove=False)

    
    def begin_conversation(self):
        print("[yellow]Starting conversation with AI...[/yellow]")
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
                        file_path = self.polly_tts_manager.text_to_speech(response, None, True, self.config['tts']['voice'], 'mp3')
                    except Exception as e:
                        print(f"[red]Error with Polly TTS: {e}[/red]")
                        print("[yellow]Falling back to Google TTS...[/yellow]")
                        file_path = self.google_tts_manager.text_to_speech(response, None)
                    
                    self.audio_manager.load_audio(file_path)

                    print(f"[yellow]Playing audio response from: audio/{os.path.basename(file_path) if file_path else 'unknown'}[/yellow]")
                    self.audio_manager.play_audio(file_path)

                    if self.obs_enabled:
                        self.obs_websockets_manager.set_source_visibility(
                            scene_name=self.config['obs']['image']['scene_name'],
                            source_name=self.config['obs']['image']['source_name'],
                            source_visible=True
                        )

                        if self.config['obs']['head']['enabled']:
                            self.obs_websockets_manager.set_source_visibility(
                                scene_name=self.config['obs']['head']['scene_name'],
                                source_name=self.config['obs']['head']['source_name'],
                                source_visible=True
                            )

                        self.obs_websockets_manager.set_filter_visibility(
                            source_name=self.config['obs']['filter']['source_name'],
                            filter_name=self.config['obs']['filter']['filter_name'],
                            filter_enabled=True
                        )
                    
                    time.sleep(self.audio_manager.get_audio_length(file_path))

                    if self.obs_enabled:
                        self.obs_websockets_manager.set_source_visibility(
                            scene_name=self.config['obs']['image']['scene_name'],
                            source_name=self.config['obs']['image']['source_name'],
                            source_visible=False
                        )

                        if self.config['obs']['head']['enabled']:
                            self.obs_websockets_manager.set_source_visibility(
                                scene_name=self.config['obs']['head']['scene_name'],
                                source_name=self.config['obs']['head']['source_name'],
                                source_visible=False
                            )

                        if self.config['obs']['filter']['enabled']:
                            self.obs_websockets_manager.set_filter_visibility(
                                source_name=self.config['obs']['filter']['source_name'],
                                filter_name=self.config['obs']['filter']['filter_name'],
                                filter_enabled=False
                            )

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

def load_config():
    """Load configuration from YAML file."""
    yaml_config_path = os.path.join(os.path.dirname(__file__), 'config.yaml')
    if not os.path.exists(yaml_config_path):
        print(f"config file not found at {yaml_config_path}. Please ensure it exists.")
        sys.exit(1)

    with open(yaml_config_path, 'r') as file:
        config = yaml.load(file, Loader=yaml.FullLoader)

    return config

if __name__ == '__main__':
    app = AIChatApp()
    app.begin_conversation()