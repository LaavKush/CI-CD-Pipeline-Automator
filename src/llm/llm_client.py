import os
import requests
from dotenv import load_dotenv

load_dotenv()

OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5-coder:7b")
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://127.0.0.1:11434")

print(f"[LLMClient] Using model: {OLLAMA_MODEL} at {OLLAMA_URL}")


class LLMClient:
    def ask(self, prompt: str) -> str:
        payload = {
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False,
            # limit how many tokens it can generate so it’s not huge/slow
            "options": {
                "num_predict": 512,   # adjust if you want longer output
            },
        }

        try:
            print("[LLMClient] Sending request to Ollama...")
            resp = requests.post(
                f"{OLLAMA_URL}/api/generate",
                json=payload,
                timeout=300,  # don’t hang forever
            )
            print("[LLMClient] HTTP status:", resp.status_code)
            resp.raise_for_status()
            data = resp.json()
            return data.get("response", "")
        except requests.exceptions.Timeout:
            return "[ERROR] LLM request timed out"
        except Exception as e:
            return f"[ERROR] LLM request failed: {e}"
