import os
import json
from pathlib import Path
from typing import List, Dict, Set, Optional
from collections import defaultdict
import yaml
from llm_client import LLMClient, CocktailInfo

class CocktailWorkflow:
    def __init__(self):
        self.client = LLMClient()
        self.base_dirs = {
            'original': Path('data/original'),
            'standardized': Path('data/standardized'),
            'reports': Path('data/reports')
        }
        
        # Create necessary directories
        for dir_path in self.base_dirs.values():
            dir_path.mkdir(parents=True, exist_ok=True)
        
        # Load name mappings
        self.name_mappings = self._load_name_mappings()
    
    def _load_name_mappings(self) -> Dict:
        """Load name mappings from configuration file"""
        mapping_file = Path('data/name_mappings.yaml')
        if mapping_file.exists():
            with open(mapping_file, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        return {}
    
    def _find_standard_name(self, category: str, name_en: str, name_zh: str) -> Optional[Dict]:
        """Find standard name and translation for a given name"""
        # Convert input name to lowercase for case-insensitive comparison
        name_en_lower = name_en.lower()
        
        # Search in all categories, not just the provided one
        for search_category, items in self.name_mappings.items():
            for key, item in items.items():
                # Check standard name (case-insensitive)
                if item['standard_en'].lower() == name_en_lower:
                    result = {
                        'en': item['standard_en'],  # Use the standard casing from mapping
                        'zh': item['standard_zh'],
                        'category': search_category  # Use the root category
                    }
                    if 'tags' in item:
                        result['tags'] = [{'en': tag['en'], 'zh': tag['zh']} for tag in item['tags']]
                    return result
                
                # Check variants (case-insensitive)
                for variant in item.get('variants', []):
                    if variant['en'].lower() == name_en_lower:
                        result = {
                            'en': item['standard_en'],  # Use the standard casing from mapping
                            'zh': item['standard_zh'],
                            'category': search_category  # Use the root category
                        }
                        if 'tags' in item:
                            result['tags'] = [{'en': tag['en'], 'zh': tag['zh']} for tag in item['tags']]
                        return result
        
        return None
    
    def fetch_cocktails(self, cocktail_names: List[str]) -> None:
        """Step 1: Fetch cocktail data and save to original directory"""
        for cocktail in cocktail_names:
            print(f"Processing {cocktail}...")
            file_path = self.base_dirs['original'] / f"{cocktail.lower().replace(' ', '_').replace('/', '-')}.json"
            
            if not file_path.exists():
                cocktail_info = self.client.get_cocktail_info(cocktail)
                if cocktail_info:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        json.dump(cocktail_info.dict(), f, ensure_ascii=False, indent=2)
                    print(f"Saved {cocktail} to {file_path}")
                else:
                    print(f"Failed to process {cocktail}")
            else:
                print(f"Skipping {cocktail}, file already exists")
    
    def generate_ingredient_report(self) -> None:
        """Step 2: Generate ingredient summary report"""
        # Load all cocktail data from standardized directory
        cocktails = []
        for file_path in self.base_dirs['standardized'].glob('*.json'):
            with open(file_path, 'r', encoding='utf-8') as f:
                cocktails.append(json.load(f))
        
        # Initialize counters with additional tag information
        # Using tuple of tuples for tags to maintain uniqueness and order
        base_spirit_counts = defaultdict(lambda: {'count': 0, 'tags': set()})
        liqueur_counts = defaultdict(lambda: {'count': 0, 'tags': set()})
        ingredient_counts = defaultdict(lambda: {'count': 0, 'tags': set()})
        flavor_counts = defaultdict(lambda: {'count': 0, 'tags': set()})
        
        # Process each cocktail
        for cocktail in cocktails:
            # Count base spirits
            for spirit in cocktail.get('base_spirits', []):
                name_en = spirit['name']['en']
                name_zh = spirit['name']['zh']
                key = (name_en, name_zh)
                base_spirit_counts[key]['count'] += 1
                # Add tags from mapping if available
                standard = self._find_standard_name('base_spirits', name_en, name_zh)
                if standard and 'tags' in standard:
                    # Convert tag dictionaries to tuples for set operations
                    tags_as_tuples = {(tag['en'], tag['zh']) for tag in standard['tags']}
                    base_spirit_counts[key]['tags'].update(tags_as_tuples)
            
            # Count liqueurs
            for liqueur in cocktail.get('liqueurs', []):
                name_en = liqueur['name']['en']
                name_zh = liqueur['name']['zh']
                key = (name_en, name_zh)
                liqueur_counts[key]['count'] += 1
                # Add tags from mapping if available
                standard = self._find_standard_name('liqueurs', name_en, name_zh)
                if standard and 'tags' in standard:
                    tags_as_tuples = {(tag['en'], tag['zh']) for tag in standard['tags']}
                    liqueur_counts[key]['tags'].update(tags_as_tuples)
            
            # Count ingredients
            for ingredient in cocktail.get('ingredients', []):
                name_en = ingredient['name']['en']
                name_zh = ingredient['name']['zh']
                key = (name_en, name_zh)
                ingredient_counts[key]['count'] += 1
                # Add tags from mapping if available
                standard = self._find_standard_name('ingredients', name_en, name_zh)
                if standard and 'tags' in standard:
                    tags_as_tuples = {(tag['en'], tag['zh']) for tag in standard['tags']}
                    ingredient_counts[key]['tags'].update(tags_as_tuples)
            
            # Count flavor descriptors
            for flavor in cocktail.get('flavor_descriptors', []):
                name_en = flavor['en']
                name_zh = flavor['zh']
                key = (name_en, name_zh)
                flavor_counts[key]['count'] += 1
                # Add tags from mapping if available
                standard = self._find_standard_name('flavor_descriptors', name_en, name_zh)
                if standard and 'tags' in standard:
                    tags_as_tuples = {(tag['en'], tag['zh']) for tag in standard['tags']}
                    flavor_counts[key]['tags'].update(tags_as_tuples)
        
        # Create the report structure with bilingual tags and sort by count
        def create_sorted_items(counts_dict):
            items = [
                {
                    'name': {'en': en, 'zh': zh},
                    'count': info['count'],
                    'tags': [{'en': tag_en, 'zh': tag_zh} for tag_en, tag_zh in sorted(info['tags'])] if info['tags'] else []
                }
                for (en, zh), info in counts_dict.items()
            ]
            return sorted(items, key=lambda x: (-x['count'], x['name']['en']))  # Sort by count desc, then name
        
        report = {
            'base_spirits': create_sorted_items(base_spirit_counts),
            'liqueurs': create_sorted_items(liqueur_counts),
            'ingredients': create_sorted_items(ingredient_counts),
            'flavor_descriptors': create_sorted_items(flavor_counts)
        }
        
        # Save the report
        report_file = self.base_dirs['reports'] / 'ingredient_summary.json'
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
    
    def analyze_name_mismatches(self) -> None:
        """Step 3: Analyze name mismatches and generate report"""
        # Load all cocktail data from original directory
        cocktails = []
        for file_path in self.base_dirs['original'].glob('*.json'):
            with open(file_path, 'r', encoding='utf-8') as f:
                cocktails.append(json.load(f))
        
        # Initialize mismatch tracking
        name_mismatches = {
            'base_spirits': defaultdict(set),
            'liqueurs': defaultdict(set),
            'ingredients': defaultdict(set),
            'flavor_descriptors': defaultdict(set)
        }
        
        # Track items not in mappings
        unmapped_items = {
            'base_spirits': set(),
            'liqueurs': set(),
            'ingredients': set(),
            'flavor_descriptors': set()
        }
        
        # Process each cocktail
        for cocktail in cocktails:
            # Track base spirit mismatches
            for spirit in cocktail.get('base_spirits', []):
                name_en = spirit['name']['en']
                name_zh = spirit['name']['zh']
                standard = self._find_standard_name('base_spirits', name_en, name_zh)
                if standard:
                    if standard['zh'] != name_zh:
                        name_mismatches['base_spirits'][name_en].add(name_zh)
                else:
                    unmapped_items['base_spirits'].add(name_en)
            
            # Track liqueur mismatches
            for liqueur in cocktail.get('liqueurs', []):
                name_en = liqueur['name']['en']
                name_zh = liqueur['name']['zh']
                standard = self._find_standard_name('liqueurs', name_en, name_zh)
                if standard:
                    if standard['zh'] != name_zh:
                        name_mismatches['liqueurs'][name_en].add(name_zh)
                else:
                    unmapped_items['liqueurs'].add(name_en)
            
            # Track ingredient mismatches
            for ingredient in cocktail.get('ingredients', []):
                name_en = ingredient['name']['en']
                name_zh = ingredient['name']['zh']
                standard = self._find_standard_name('ingredients', name_en, name_zh)
                if standard:
                    if standard['zh'] != name_zh:
                        name_mismatches['ingredients'][name_en].add(name_zh)
                else:
                    unmapped_items['ingredients'].add(name_en)
            
            # Track flavor descriptor mismatches
            for flavor in cocktail.get('flavor_descriptors', []):
                name_en = flavor['en']
                name_zh = flavor['zh']
                standard = self._find_standard_name('flavor_descriptors', name_en, name_zh)
                if standard:
                    if standard['zh'] != name_zh:
                        name_mismatches['flavor_descriptors'][name_en].add(name_zh)
                else:
                    unmapped_items['flavor_descriptors'].add(name_en)
        
        # Create the mismatch report
        mismatch_report = {
            'mismatches': {},
            'unmapped_items': {}
        }
        
        # Add mismatches
        for category, items in name_mismatches.items():
            category_mismatches = {}
            for name_en, name_zh_set in items.items():
                if len(name_zh_set) > 1:
                    category_mismatches[name_en] = list(name_zh_set)
            if category_mismatches:
                mismatch_report['mismatches'][category] = category_mismatches
        
        # Add unmapped items
        for category, items in unmapped_items.items():
            if items:
                mismatch_report['unmapped_items'][category] = list(items)
        
        # Save the mismatch report
        mismatch_file = self.base_dirs['reports'] / 'name_mismatches.yaml'
        with open(mismatch_file, 'w', encoding='utf-8') as f:
            yaml.dump(mismatch_report, f, allow_unicode=True, sort_keys=False)
    
    def standardize_names(self) -> None:
        """Standardize names in all cocktail files using the mappings"""
        for file_path in self.base_dirs['original'].glob('*.json'):
            with open(file_path, 'r', encoding='utf-8') as f:
                cocktail = json.load(f)
            
            # Create a copy of the cocktail data for standardization
            standardized_cocktail = cocktail.copy()
            
            # Initialize category lists if they don't exist
            for category in ['base_spirits', 'liqueurs', 'ingredients']:
                if category not in standardized_cocktail:
                    standardized_cocktail[category] = []
            
            # Temporary storage for categorized items
            categorized_items = {
                'base_spirits': [],
                'liqueurs': [],
                'ingredients': []
            }
            
            # Process all items from all categories
            for category in ['base_spirits', 'liqueurs', 'ingredients']:
                for item in standardized_cocktail.get(category, []):
                    name_en = item['name']['en']
                    name_zh = item['name']['zh']
                    standard = self._find_standard_name(category, name_en, name_zh)
                    
                    if standard:
                        # Create standardized item
                        standardized_item = item.copy()
                        standardized_item['name'] = {
                            'en': standard['en'],
                            'zh': standard['zh']
                        }
                        if 'tags' in standard:
                            standardized_item['tags'] = standard['tags']
                        
                        # Add to the correct category based on mapping root
                        target_category = standard['category']
                        categorized_items[target_category].append(standardized_item)
                    else:
                        # Keep item in original category if no mapping found
                        categorized_items[category].append(item)
            
            # Update cocktail with categorized items
            for category, items in categorized_items.items():
                standardized_cocktail[category] = items
            
            # Process flavor descriptors separately since they have a different structure
            if 'flavor_descriptors' in standardized_cocktail:
                for flavor in standardized_cocktail['flavor_descriptors']:
                    standard = self._find_standard_name('flavor_descriptors', flavor['en'], flavor['zh'])
                    if standard:
                        flavor['en'] = standard['en']
                        flavor['zh'] = standard['zh']
            
            # Save the standardized cocktail data
            standardized_file = self.base_dirs['standardized'] / file_path.name
            with open(standardized_file, 'w', encoding='utf-8') as f:
                json.dump(standardized_cocktail, f, ensure_ascii=False, indent=2)
            
            print(f"Saved standardized version of {file_path.name} to {standardized_file}")
    
    def run_workflow(self, cocktail_names: List[str], standardize: bool = False) -> None:
        """Run the complete workflow"""
        print("Step 1: Fetching cocktail data...")
        self.fetch_cocktails(cocktail_names)
        
        print("Step 2: Generating ingredient report...")
        self.generate_ingredient_report()
        
        print("Step 3: Analyzing name mismatches...")
        self.analyze_name_mismatches()
        
        if standardize:
            print("Step 4: Standardizing names...")
            self.standardize_names()
            print("Regenerating reports after standardization...")
            self.generate_ingredient_report()
            self.analyze_name_mismatches()
        
        print("Workflow completed!")

if __name__ == '__main__':
    # Initialize the workflow
    workflow = CocktailWorkflow()
    
    # Use the cocktail list from main.py
    cocktails = [
        "Garibaldi", "Jungle Bird", "Enzoni", "Siesta", "Bicicletta", "Cardinale", "Milano-Torino", 
        "The Left Hand", "Old Pal", "Sorrentino", "The Ribbon", "Sloegroni", "Old Acquaintance", 
        "Old Gal", "Killer Cocktail", "English Marmalade", "Jasmine", "Paris Between the Wars", 
        "Spaghett", "Blood and Sand", "Remember the Maine", "Little Italy", "Liberal Cocktail", 
        "Brooklyn Cocktail", "Bobby Burns", "Bamboo Cocktail", "Americano", "Vieux Carré", 
        "Million Dollar Cocktail", "Liberal Cocktail", "Horsefeather", "Between the Sheets", 
        "Corpse Reviver #2", "Champagne Cocktail", "Penicillin", "Cardinale", "Old Pal", "Enzoni", 
        "The Left Hand", "Adonis", "Income Tax Cocktail", "Maiden's Prayer", "Chrysanthemum", 
        "20th Century Cocktail", "Alexandre", "Bronx Cocktail", "Dukes Martini", "El Presidente", 
        "Ford Cocktail", "Harvard Cocktail", "Ideal Cocktail", "Piccadilly Cocktail", "Silver Streak", 
        "Turf Club Cocktail", "Upside Down Martini", "Yale Cocktail", "Bijou Cocktail", "Dry Rob Roy", 
        "Savoy Corpse Reviver", "Black Russian", "White Russian", "Espresso Martini", "Brave Bull", 
        "Colorado Bulldog", "Mind Eraser", "Flying Grasshopper", "Blind Russian", "Russian Quaalude", 
        "Toasted Almond", "Reverend's Daughter", "Kahlúa and Cream", "Kahlúa Fizz", "Kahlúa Sour", 
        "Kahlúa Alexander", "Kahlúa Hot Chocolate", "Kahlúa Mudslide", "Kahlúa Stinger", "Kahlúa Frappe", 
        "Dirty Mother", "B-52", "Chocolate Martini", "Irish Coffee", "Baileys Hot Chocolate", 
        "Baileys Alexander", "Baileys White Russian", "Baileys Mudslide", "Baileys Frappé", 
        "Baileys and Coffee", "Baileys and Cream Soda", "Baileys and Milk", "Baileys and Frangelico", 
        "Baileys and Amaretto", "Baileys and Mint Chocolate", "Baileys and Hazelnut Liqueur", 
        "Baileys and Vodka Shot", "Baileys and Brandy", "Baileys and Dark Rum", 
        "Baileys and Butterscotch Schnapps", "Baileys and Ice Cream"
    ]
    
    # Run the workflow with standardization
    workflow.run_workflow(cocktails, standardize=True) 