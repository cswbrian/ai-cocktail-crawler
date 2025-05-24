from dotenv import load_dotenv
import os

def load_environment():
    """Load the appropriate environment file based on ENVIRONMENT variable"""
    env = os.getenv("ENVIRONMENT", "development")
    env_file = f".env.{env}"
    
    # First try to load the specific environment file
    if os.path.exists(env_file):
        load_dotenv(env_file, override=True)
        print(f"Loaded environment from {env_file}")
    else:
        # Fallback to .env if specific file doesn't exist
        if os.path.exists(".env"):
            load_dotenv(".env", override=True)
            print("Loaded environment from .env")
        else:
            raise FileNotFoundError(f"Environment file {env_file} or .env not found")
    
    # Verify required environment variables are set
    required_vars = [
        "API_KEY",
        "SUPABASE_URL",
        "SUPABASE_KEY"
    ]
    
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    if missing_vars:
        raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")

# Load environment variables
load_environment()

# Gemini API configuration
API_KEY = os.getenv('API_KEY')

# Model configuration
MODEL_NAME = "gemini-pro"  # Default model to use
