from supabase import create_client
from config import SUPABASE_URL, SUPABASE_KEY, validate_config


valid, message = validate_config()

if not valid:
    raise ValueError(message)


supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)