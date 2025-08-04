import os
import sys
import yaml
import dotenv
from utils import *

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
        self.speech_to_text = SpeechToText()
        self.gemini_ai_manager = GeminiAIManager(
            api_key=os.getenv("GEMINI_API_KEY"),
            model=config['ai']['model'],
            system_instruction=config['ai']['system_instruction']
        )

if __name__ == '__main__':
    app = AIChatApp()
    print("AI Chat App initialized successfully.")