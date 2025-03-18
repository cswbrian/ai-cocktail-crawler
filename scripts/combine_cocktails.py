import json
from pathlib import Path

def combine_cocktails():
    # Path to the JSON directory
    json_dir = Path('data/standardized')
    
    # Get all JSON files in the directory
    json_files = json_dir.glob('*.json')
    
    # Initialize an empty list to hold all cocktails
    cocktails = []
    
    # Read each JSON file and append its content to the list
    for json_file in json_files:
        with open(json_file, 'r') as f:
            cocktail_data = json.load(f)
            cocktails.append(cocktail_data)
    
    # Save the combined list to cocktails.json
    output_file = Path('cocktails.json')
    with open(output_file, 'w') as f:
        json.dump(cocktails, f, indent=2)
    
    print(f"Combined {len(cocktails)} cocktails into {output_file}")

if __name__ == "__main__":
    combine_cocktails() 