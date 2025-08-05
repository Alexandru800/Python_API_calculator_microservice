from dotenv import load_dotenv
import os
from pathlib import Path

# Load .env file located at project root
load_dotenv(dotenv_path=Path(__file__).resolve().parents[2] / ".env")

# Load settings with fallbacks
API_KEY: str = os.getenv("API_KEY", "default_key")
DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./app/database.db")
DEBUG: bool = os.getenv("DEBUG", "False").lower() in ("true", "1", "yes")
