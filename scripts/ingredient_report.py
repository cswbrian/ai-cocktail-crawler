import json
from collections import defaultdict
from pathlib import Path

def generate_ingredient_report():
    # Load the cocktails data
    cocktails_file = Path('cocktails.json')
    with open(cocktails_file, 'r', encoding='utf-8') as f:
        cocktails = json.load(f)
    
    # Initialize counters
    unique_cocktails = set()
    base_spirits = []
    liqueurs = []
    ingredients = []
    flavor_descriptors = []
    
    # Temporary storage for counts
    base_spirit_counts = defaultdict(int)
    liqueur_counts = defaultdict(int)
    ingredient_counts = defaultdict(int)
    flavor_counts = defaultdict(int)
    
    # Process each cocktail
    for cocktail in cocktails:
        # Add cocktail names
        unique_cocktails.add((cocktail['name']['en'], cocktail['name']['zh']))
        
        # Count base spirits
        for spirit in cocktail.get('base_spirits', []):
            name_en = spirit['name']['en']
            name_zh = spirit['name']['zh']
            base_spirit_counts[(name_en, name_zh)] += 1
        
        # Count liqueurs
        for liqueur in cocktail.get('liqueurs', []):
            name_en = liqueur['name']['en']
            name_zh = liqueur['name']['zh']
            liqueur_counts[(name_en, name_zh)] += 1
        
        # Count ingredients
        for ingredient in cocktail.get('ingredients', []):
            name_en = ingredient['name']['en']
            name_zh = ingredient['name']['zh']
            ingredient_counts[(name_en, name_zh)] += 1
        
        # Count flavor descriptors
        for flavor in cocktail.get('flavor_descriptors', []):
            name_en = flavor['en']
            name_zh = flavor['zh']
            flavor_counts[(name_en, name_zh)] += 1
    
    # Convert counts to the desired structure
    unique_cocktails = [{
        'en': en,
        'zh': zh
    } for en, zh in sorted(unique_cocktails)]
    
    base_spirits = [{
        'name': {'en': en, 'zh': zh},
        'count': count
    } for (en, zh), count in base_spirit_counts.items()]
    
    liqueurs = [{
        'name': {'en': en, 'zh': zh},
        'count': count
    } for (en, zh), count in liqueur_counts.items()]
    
    ingredients = [{
        'name': {'en': en, 'zh': zh},
        'count': count
    } for (en, zh), count in ingredient_counts.items()]
    
    flavor_descriptors = [{
        'name': {'en': en, 'zh': zh},
        'count': count
    } for (en, zh), count in flavor_counts.items()]
    
    # Create the report structure
    report = {
        'unique_cocktails': unique_cocktails,
        'base_spirits': sorted(base_spirits, key=lambda x: x['count'], reverse=True),
        'liqueurs': sorted(liqueurs, key=lambda x: x['count'], reverse=True),
        'ingredients': sorted(ingredients, key=lambda x: x['count'], reverse=True),
        'flavor_descriptors': sorted(flavor_descriptors, key=lambda x: x['count'], reverse=True)
    }
    
    # Save the report
    report_file = Path('ingredient_report.json')
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print("Generated ingredient report with the requested structure")

if __name__ == '__main__':
    generate_ingredient_report() 