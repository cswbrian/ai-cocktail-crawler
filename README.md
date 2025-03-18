# Cocktail Crawler Project

This project is a cocktail information crawler that fetches detailed cocktail recipes and information using the Gemini API, with support for standardization and bilingual data processing.

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

6. **Set up name mappings**
   - Create a `data/name_mappings.yaml` file for ingredient standardization
   - Define mappings for base spirits, liqueurs, ingredients, and flavor descriptors

7. **Run the project**
   ```bash
   python workflow.py
   ```

## Project Structure

- `workflow.py`: Main workflow script that handles data processing and standardization
- `llm_client.py`: Handles API communication with Gemini
- `config.py`: Contains API configuration (you need to create this)
- `data/`: Project data directory structure:
  - `original/`: Raw cocktail data from API
  - `standardized/`: Standardized cocktail data
  - `reports/`: Generated analysis reports
  - `name_mappings.yaml`: Ingredient name standardization mappings

## Key Features

- Fetches detailed cocktail information including:
  - Base spirits
  - Liqueurs
  - Ingredients
  - Preparation techniques
  - Flavor profiles
- Standardizes ingredient names and categories
- Generates detailed reports:
  - Ingredient usage summary
  - Name mismatch analysis
- Supports bilingual information (English and Traditional Chinese)
- Automatic ingredient categorization and standardization

## Requirements

The project uses the following Python packages:
- google-genai==0.8.4
- PyYAML==6.0.2
- requests==2.31.0
- python-dotenv==1.0.0

## Workflow Steps

1. **Data Fetching**: Retrieves cocktail information from the Gemini API
2. **Name Standardization**: Standardizes ingredient names using predefined mappings
3. **Report Generation**: 
   - Generates ingredient usage summaries
   - Analyzes name mismatches
   - Creates standardized data files

## Troubleshooting

- If you encounter API key issues, verify your key configuration in `config.py`
- Ensure you have proper write permissions for the `data` directory and its subdirectories
- Check that your `name_mappings.yaml` file is properly formatted

## License

This project is licensed under the MIT License - see the LICENSE file for details.
