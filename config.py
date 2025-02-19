from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Gemini API configuration
API_KEY = os.getenv('API_KEY')

# Model configuration
MODEL_NAME = "gemini-pro"  # Default model to use
