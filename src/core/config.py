# src/core/config.py
from dotenv import load_dotenv
import os

load_dotenv()  # loads .env from repo root if present

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_USER = os.getenv("GITHUB_USER")
GITHUB_API_URL = os.getenv("GITHUB_API_URL", "https://api.github.com")
CLONE_WORKDIR = os.getenv("CLONE_WORKDIR", "./workspace")
from pydantic import BaseSettings

class Settings(BaseSettings):
    github_token: str
    openai_api_key: str | None = None
    ollama_endpoint: str = "http://localhost:11434"
    poll_interval: int = 5  # seconds

    class Config:
        env_file = ".env"

settings = Settings()
