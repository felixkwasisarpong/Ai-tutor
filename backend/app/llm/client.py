import requests 
from requests.exceptions import Timeout,RequestException
class OllamaClient:
    def __init__(self, base_url: str = "http://localhost:11434", model: str = "llama3"):
        self.base_url = base_url
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
                f"{self.base_url}/api/generate", json=payload,timeout=30
            )
            response.raise_for_status()
            data = response.json()
            return data.get("response", "").strip()

        except Timeout:
            return "Error: The request to the LLM server timed out."
        except RequestException as e:
            return f"Error: An error occurred while communicating with the LLM server: {str(e)}"