# Cocktail Crawler Project

This project is a cocktail information crawler that fetches detailed cocktail recipes and information using the Gemini API, with support for standardization, bilingual data processing, and automatic cocktail categorization.

## Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.7 or higher
- pip (Python package manager)

## Database Integration

The project uses Supabase as its database backend. The database schema is designed for maintainability and scalability, featuring:

- UUID-based primary keys for all tables
- Normalized table structure for efficient data management
- Support for multilingual content (English and Traditional Chinese)
- Comprehensive cocktail information storage including:
  - Base spirits and liqueurs
  - Ingredients and measurements
  - Preparation techniques
  - Flavor profiles
  - Categories and tags

### Database Setup

1. Create a Supabase project at https://supabase.com
2. Set up your environment variables:
   - Create a `.env` file in the project root
   - Add your Supabase credentials:
     ```
     SUPABASE_URL=your_supabase_project_url
     SUPABASE_KEY=your_supabase_anon_key
     ```

### Database Schema

The database consists of the following tables:
- `cocktails`: Main cocktail information
- `base_spirits`: Base spirit types and details
- `liqueurs`: Liqueur types and details
- `ingredients`: Standardized ingredient information
- `cocktail_ingredients`: Junction table for cocktail-ingredient relationships
- `preparation_techniques`: Standardized preparation methods
- `flavor_profiles`: Cocktail flavor characteristics
- `categories`: Cocktail categories
- `cocktail_categories`: Junction table for cocktail-category relationships

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

## Adding New Cocktails

There are two ways to add cocktails:

1. **Using main.py (Recommended for specific cocktails)**
   - Edit `main.py` and add cocktail names to the `new_cocktails` list
   - Run `python main.py`

2. **Using workflow.py (For processing all cocktails)**
   - Place cocktail JSON files in `data/original/`
   - Run `python workflow.py`

## Project Structure

- `workflow.py`: Main workflow script that handles data processing and standardization
- `llm_client.py`: Handles API communication with Gemini and cocktail categorization
- `main.py`: Script for adding new cocktails
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
  - Categories
- Automatic cocktail categorization into:
  - Strong & Spirit-Focused
  - Sweet & Tart
  - Tall & Bubbly
  - Rich & Creamy
- Standardizes ingredient names and categories
- Supports bilingual information (English and Traditional Chinese)
- Generates detailed reports

## Cocktail Categories

Each cocktail is automatically categorized based on its characteristics:
1. **Strong & Spirit-Focused**: Spirit-forward cocktails
2. **Sweet & Tart**: Balanced sweet-sour cocktails
3. **Tall & Bubbly**: Carbonated highballs
4. **Rich & Creamy**: Creamy/eggy cocktails

Categories are determined by analyzing:
- The cocktail's description
- Base spirit and its amount
- Sweet/sour ingredients
- Carbonation presence
- Cream/egg ingredients

## Requirements

The project uses the following Python packages:
- google-genai==0.8.4
- PyYAML==6.0.2
- pydantic
- requests==2.31.0

## Workflow Steps

1. **Data Fetching**: 
   - Checks if cocktail exists in data/original/
   - If not, fetches from Gemini API
   - Saves new cocktails to data/original/
2. **Categorization**:
   - Automatically determines cocktail categories
   - Uses LLM to analyze cocktail characteristics
3. **Standardization**:
   - Standardizes ingredient names
   - Generates reports and analysis

## Output Files

- `cocktails.json`: Combined file containing all standardized cocktail data
- `data/reports/summary.json`: Summary of ingredient usage
- `data/reports/name_mismatches.yaml`: Analysis of naming inconsistencies
- Individual cocktail files in `data/standardized/` directory

## Troubleshooting

- If you encounter API key issues, verify your key configuration in `config.py`
- Ensure you have proper write permissions for the `data` directory and its subdirectories
- Check that your `name_mappings.yaml` file is properly formatted

## License

This project is licensed under the MIT License - see the LICENSE file for details.
