# src/core/config.py
from dotenv import load_dotenv
import os

load_dotenv()  # loads .env from repo root if present

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_USER = os.getenv("GITHUB_USER")
GITHUB_API_URL = os.getenv("GITHUB_API_URL", "https://api.github.com")
CLONE_WORKDIR = os.getenv("CLONE_WORKDIR", "./workspace")
