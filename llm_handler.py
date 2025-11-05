import ollama
from config import cfg

class LLMHandler:
    def __init__(self):
        self.model_name = cfg.OLLAMA_MODEL_NAME
        self.base_url = cfg.OLLAMA_BASE_URL
        self.system_prompt = cfg.SYSTEM_PROMPT
        self.conversation_history = []
        if self.system_prompt: self.conversation_history.append({"role": "system", "content": self.system_prompt})
        try:
            # print(f"LLM: Initializing Ollama client for model '{self.model_name}' at {self.base_url}...")
            self.client = ollama.Client(host=self.base_url)
            self.client.show(self.model_name) # Verify model exists
            # print(f"LLM: Successfully connected to Ollama and model '{self.model_name}' is available.")
        except Exception as e: print(f"LLM: Failed to connect/find model '{self.model_name}': {e}"); raise
    def get_response(self, user_prompt_text):
        if not user_prompt_text:
            response = "I didn't quite catch that. Could you please say it again?"
            print(f"{cfg.AI_NAME}: {response}"); return response # LLM handler prints AI response
        self.conversation_history.append({"role": "user", "content": user_prompt_text})
        try:
            response_stream = self.client.chat(model=self.model_name, messages=self.conversation_history, stream=True)
            ai_full_response = ""; print(f"{cfg.AI_NAME}: ", end="", flush=True) # Prefix for streaming
            for chunk in response_stream:
                if 'message' in chunk and 'content' in chunk['message']:
                    token = chunk['message']['content']; ai_full_response += token; print(token, end="", flush=True)
                if chunk.get('done'): print(); break # Newline after stream
            if not ai_full_response.strip():
                ai_full_response = "I'm not sure how to respond to that."
                print(f"{cfg.AI_NAME}: {ai_full_response}") # Ensure it's printed if stream was empty
            self.conversation_history.append({"role": "assistant", "content": ai_full_response.strip()})
            return ai_full_response.strip()
        except Exception as e:
            print(f"\nLLM: Error getting response: {e}")
            if self.conversation_history and self.conversation_history[-1]["role"] == "user": self.conversation_history.pop()
            response = "I'm having a little trouble thinking. Please try again."
            print(f"{cfg.AI_NAME}: {response}"); return response
    def clear_history(self):
        # print("LLM: Clearing conversation history.") # User gets feedback via TTS
        self.conversation_history = []
        if self.system_prompt: self.conversation_history.append({"role": "system", "content": self.system_prompt})