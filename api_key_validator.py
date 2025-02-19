from google import genai
from config import API_KEY

def validate_api_key(api_key: str) -> bool:
    """
    Validates if the provided API key works with the LLM service.
    
    Args:
        api_key (str): The API key to validate
        
    Returns:
        bool: True if the API key is valid, False otherwise
    """
    try:
        # Create a test client with the provided API key
        test_client = genai.Client(api_key=API_KEY)
        
        # Make a simple test request
        test_client.models.generate_content(
            model='gemini-2.0-flash',
            contents="Test",
            config={
                'response_mime_type': 'text/plain'
            }
        )
        return True
    except Exception as e:
        print(f"API key validation failed: {str(e)}")
        return False

if __name__ == "__main__":
    # Example usage when run directly
    from config import API_KEY
    
    if validate_api_key(API_KEY):
        print("API key is valid!")
    else:
        print("API key is invalid.") 