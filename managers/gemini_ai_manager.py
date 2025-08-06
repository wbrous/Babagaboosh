from google import genai
from google.genai import types
from rich import print

class GeminiAIManager:
    def __init__(self, model="gemini-2.0-flash-lite", system_instruction="You are a helpful AI assistant.", max_context_length=1048576, api_key=None):
        """Initialize the Gemini AI Manager with an API key."""

        # Validate the API key
        self.api_key = api_key
        if not self.api_key:
            raise ValueError("API key must be provided for GeminiAIManager.")
        
        try:
            self.client = genai.Client(
                api_key=self.api_key,
            )
        except Exception as e:
            raise RuntimeError(f"Failed to initialize Gemini AI client: {e}")

        self.model = model
        self.max_context_length = max_context_length
        self.chat_history = []
        self.system_instruction = system_instruction

    def clear_chat_history(self):
        """Clear the chat history."""
        self.chat_history = []

    def trim_chat_history(self):
        """Trim the chat history to fit within the maximum context length."""
        if not self.chat_history:
            return
        
        # Trim oldest entries until context is within limit
        while True:
            current_length = self.get_chat_context_length()
            if not current_length or current_length <= self.max_context_length * 0.9:
                break
            self.chat_history.pop(0)

    def get_chat_history(self):
        """Get the current chat history."""
        return self.chat_history
    
    def get_chat_context_length(self):
        """Get the current context length (in tokens) of the chat context."""
        if not self.chat_history:
            return 0
            
        try:
            token_count_response = self.client.models.count_tokens(
                model=self.model,
                contents=self.chat_history
            )
            
            return token_count_response.total_tokens
            
        except Exception as e:
            print(f"[yellow]Warning: Could not get accurate token count, falling back to word estimate: {e}[/yellow]")
            # Fallback to word-based estimation (roughly 1 token per 0.75 words for English)
            word_count = 0
            for content in self.chat_history:
                for part in getattr(content, 'parts', []):
                    text = getattr(part, 'text', '')
                    word_count += len(text.split())
            return int(word_count * 1.33)  # Convert words to approximate tokens

    def count_tokens_for_text(self, text):
        """Count tokens for a specific text input."""
        try:
            content = types.Content(
                role='user',
                parts=[types.Part.from_text(text=text)]
            )
            
            token_count_response = self.client.models.count_tokens(
                model=self.model,
                contents=[content]
            )
            
            return token_count_response.total_tokens
            
        except Exception as e:
            print(f"[yellow]Warning: count_tokens_for_text failed, falling back to word estimate: {e}[/yellow]")
            # Fallback to word-based estimation
            word_count = len(text.split())
            return int(word_count * 1.33)

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

        context_length = self.get_chat_context_length()
        if context_length and context_length > self.max_context_length * 0.9:
            print("[yellow]Chat history exceeds maximum context length, trimming history...[/yellow]")
            self.trim_chat_history()
            

    def generate_response(self, user_input, show_token_usage=True):
        """Generate a response from the AI model based on user input."""

        if not self.chat_history:
            print("[yellow]Chat history is empty. This is probably fine, but if you see this message again, you have a problem.[/yellow]")

        try:

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

            # Show token usage if requested (using response metadata)
            # Will capture prompt and response token counts directly from the API
            response = self.client.models.generate_content(
                model=self.model,
                contents=contents,
                config=generate_content_config,
            )
            if show_token_usage:
                meta = getattr(response, 'usage_metadata', None)
                if meta:
                    print(
                        f"[dim]Token usage (API): Prompt={meta.prompt_token_count}, "
                        f"Response={meta.candidates_token_count}, Total={meta.total_token_count}[/dim]"
                    )

            # ... existing code above handles token usage

            ai_response = response.text
            if not ai_response:
                raise RuntimeError("Received empty response from AI model")
            self.add_to_chat_history(user_input, ai_response)
            
            # Show response token count if requested
            if show_token_usage:
                response_tokens = self.count_tokens_for_text(ai_response)
                print(f"[dim]Response tokens: {response_tokens}[/dim]")
            
            return ai_response

        except Exception as e:
            if "overloaded" in str(e).lower() or "rate limit" in str(e).lower():
                print(f"[red]Model appears to be overloaded or rate limited: {e}[/red]")
                return "I'm currently overloaded, please try again later."
            raise RuntimeError(f"Failed to generate response: {e}")
