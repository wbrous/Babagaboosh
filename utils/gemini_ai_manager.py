import os
from google import genai
from google.genai import types
from rich import print

class GeminiAIManager:
    def __init__(self, model="gemini-2.0-flash-lite", system_instruction="You are a helpful AI assistant.", api_key=None):
        """Initialize the Gemini AI Manager with an API key."""

        # Validate the API key
        self.api_key = api_key
        if not self.api_key:
            raise ValueError("API key must be provided for GeminiAIManager.")
        
        try:
            client = genai.Client(
                api_key=self.api_key,
            )
        except Exception as e:
            raise RuntimeError(f"Failed to initialize Gemini AI client: {e}")

        self.model = model
        self.chat_history = []
        self.system_instruction = system_instruction

    def clear_chat_history(self):
        """Clear the chat history."""
        self.chat_history = []

    def add_to_chat_history(self, user_input, ai_response):
        """Add a user input and AI response to the chat history."""
        self.chat_history.append(
            types.Content(
                role='user',
                parts=[
                    types.Part.from_text(text=user_input)
                ]
            )
        )

        self.chat_history.append(
            types.Content(
                role='model',
                parts=[
                    types.Part.from_text(text=ai_response)
                ]
            )
        )

    def generate_response(self, user_input):
        """Generate a response from the AI model based on user input."""

        if not self.chat_history:
            print("[yellow]Chat history is empty. This is probably fine, but if you see this message again, you have a problem.[/yellow]")

        try:
            client = genai.Client(
                api_key=self.api_key,
            )

            contents = self.chat_history + [
                types.Content(
                    role='user',
                    parts=[
                        types.Part.from_text(text=user_input)
                    ]
                )
            ]

            generate_content_config = types.GenerateContentConfig(
                system_instruction=[
                    types.Part.from_text(text=self.system_instruction)
                ],
            )

            response = client.models.generate_content(
                model=self.model,
                contents=contents,
                config=generate_content_config,
            )

            ai_response = response.text
            self.add_to_chat_history(user_input, ai_response)
            return ai_response

        except Exception as e:
            raise RuntimeError(f"Failed to generate response: {e}")
