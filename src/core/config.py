from pydantic import BaseSettings

class Settings(BaseSettings):
    github_token: str
    openai_api_key: str | None = None
    ollama_endpoint: str = "http://localhost:11434"
    poll_interval: int = 5  # seconds

    class Config:
        env_file = ".env"

settings = Settings()
