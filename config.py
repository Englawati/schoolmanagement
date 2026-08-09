import os
from pathlib import Path
from dotenv import load_dotenv


# Project directory
BASE_DIR = Path(__file__).resolve().parent

# Load .env file
ENV_FILE = BASE_DIR / ".env"
load_dotenv(ENV_FILE)


# Supabase configuration
SUPABASE_URL = os.getenv("SUPABASE_URL", "").strip()
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "").strip()


def validate_config():
    """Validate Supabase configuration."""

    if not SUPABASE_URL:
        return False, "SUPABASE_URL is missing in .env"

    if not SUPABASE_KEY:
        return False, "SUPABASE_KEY is missing in .env"

    if not SUPABASE_URL.startswith("https://"):
        return False, "Invalid SUPABASE_URL. It must start with https://"

    if ".supabase.co" not in SUPABASE_URL:
        return False, "Invalid Supabase project URL"

    return True, ""