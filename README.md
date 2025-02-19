# Cocktail Crawler Project

This project is a cocktail information crawler that fetches detailed cocktail recipes and information using the Gemini API.

## Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.7 or higher
- pip (Python package manager)

## Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/cocktail-crawler.git
   cd cocktail-crawler
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Set up API Key**
   - Create a `config.py` file in the project root
   - Add your Gemini API key:
     ```python
     # Gemini API configuration
     API_KEY = "your_api_key_here"
     ```

6. **Run the project**
   ```bash
   python main.py
   ```

## Project Structure

- `main.py`: Main script to fetch and save cocktail data
- `llm_client.py`: Handles API communication with Gemini
- `config.py`: Contains API configuration (you need to create this)
- `data/cocktails/`: Directory where individual cocktail JSON files are stored
- `scripts/`: Contains utility scripts for processing cocktail data

## Key Features

- Fetches detailed cocktail information including:
  - Ingredients
  - Preparation techniques
  - Historical references
  - Flavor profiles
- Stores data in JSON format
- Supports bilingual information (English and Traditional Chinese)

## Requirements

The project uses the following Python packages (automatically installed via requirements.txt):

## Troubleshooting

- If you encounter API key issues, use the `api_key_validator.py` script to verify your key:
  ```bash
  python api_key_validator.py
  ```

- Ensure you have proper write permissions for the `data/cocktails` directory

## License

This project is licensed under the MIT License - see the LICENSE file for details.
