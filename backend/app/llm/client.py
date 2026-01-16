import requests 
from requests.exceptions import Timeout,RequestException
import os
class OllamaClient:
    def __init__(self, model: str = "llama3"):
        self.base_url = os.getenv(
            "OLLAMA_BASE_URL",
            "http://127.0.0.1:11434"
        )
        self.model = model


    def generate(self, prompt: str) -> str:
        url = f"{self.base_url}/api/generate"
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }

        try:
            response = requests.post(
                f"{self.base_url}/api/generate", json=payload,timeout=300
            )
            response.raise_for_status()
            data = response.json()
            return data.get("response", "").strip()

        except Timeout:
            return "Error: The request to the LLM server timed out."
        except RequestException as e:
            return f"Error: An error occurred while communicating with the LLM server: {str(e)}"