import os
from supabase import create_client, Client
from typing import Dict, Optional, List
import uuid

class SupabaseClient:
    def __init__(self, env: str = None):
        # If env is not specified, try to get it from environment variable
        if env is None:
            env = os.environ.get("ENVIRONMENT", "development")
        
        # Get the appropriate environment variables based on the environment
        if env == "production":
            url = os.environ.get("SUPABASE_URL_PROD")
            key = os.environ.get("SUPABASE_KEY_PROD")
        else:  # development
            url = os.environ.get("SUPABASE_URL")
            key = os.environ.get("SUPABASE_KEY")
            
        if not url or not key:
            raise ValueError(f"Supabase credentials for {env} environment must be set")
            
        self.client: Client = create_client(url, key)
        self.env = env

    def _get_or_create_unit(self, name_en: str, name_zh: str) -> Optional[str]:
        """Get or create a unit and return its ID"""
        try:
            # Try to find existing unit
            result = self.client.table('units').select('id').eq('name_en', name_en).eq('name_zh', name_zh).execute()
            
            if result.data:
                return result.data[0]['id']
            
            # Create new unit if not found
            new_unit = {
                'name_en': name_en,
                'name_zh': name_zh
            }
            result = self.client.table('units').insert(new_unit).execute()
            return result.data[0]['id'] if result.data else None
            
        except Exception as e:
            print(f"Error handling unit {name_en}: {str(e)}")
            return None

    def _get_or_create_ingredient(self, name_en: str, name_zh: str, type: str) -> Optional[str]:
        """Get or create an ingredient and return its ID"""
        try:
            # Try to find existing ingredient
            result = self.client.table('ingredients').select('id').eq('name_en', name_en).eq('name_zh', name_zh).eq('type', type).execute()
            
            if result.data:
                return result.data[0]['id']
            
            # Create new ingredient if not found
            new_ingredient = {
                'name_en': name_en,
                'name_zh': name_zh,
                'type': type
            }
            result = self.client.table('ingredients').insert(new_ingredient).execute()
            return result.data[0]['id'] if result.data else None
            
        except Exception as e:
            print(f"Error handling ingredient {name_en}: {str(e)}")
            return None

    def upsert_cocktail(self, cocktail_data: Dict) -> Optional[Dict]:
        """
        Upsert a cocktail into the database.
        Returns the updated/inserted record if successful, None if failed.
        """
        try:
            # Create a copy of the data to modify
            data_copy = cocktail_data.copy()
            
            # Remove name, slug, and ingredients from the data copy
            if 'name' in data_copy:
                del data_copy['name']
            if 'slug' in data_copy:
                del data_copy['slug']
            if 'base_spirits' in data_copy:
                del data_copy['base_spirits']
            if 'liqueurs' in data_copy:
                del data_copy['liqueurs']
            if 'ingredients' in data_copy:
                del data_copy['ingredients']
            
            # Prepare the cocktail data
            cocktail_record = {
                'name': cocktail_data['name'],
                'data': data_copy,  # Use the modified data copy
                'is_custom': False
            }

            # Upsert the cocktail
            result = self.client.table('cocktails').upsert(cocktail_record).execute()
            
            if not result.data:
                return None
                
            cocktail_id = result.data[0]['id']
            
            # Handle ingredients
            self._handle_cocktail_ingredients(cocktail_id, cocktail_data)
            
            return result.data[0]
            
        except Exception as e:
            print(f"Error upserting cocktail: {str(e)}")
            return None

    def _handle_cocktail_ingredients(self, cocktail_id: str, cocktail_data: Dict) -> None:
        """Handle the cocktail ingredients and their relationships"""
        try:
            # Process base spirits
            for spirit in cocktail_data.get('base_spirits', []):
                ingredient_id = self._get_or_create_ingredient(
                    spirit['name']['en'],
                    spirit['name']['zh'],
                    'base_spirit'
                )
                if ingredient_id:
                    self._upsert_cocktail_ingredient(
                        cocktail_id,
                        ingredient_id,
                        spirit.get('amount', 0),
                        spirit.get('unit', {'en': 'oz', 'zh': '盎司'})
                    )

            # Process liqueurs
            for liqueur in cocktail_data.get('liqueurs', []):
                ingredient_id = self._get_or_create_ingredient(
                    liqueur['name']['en'],
                    liqueur['name']['zh'],
                    'liqueur'
                )
                if ingredient_id:
                    self._upsert_cocktail_ingredient(
                        cocktail_id,
                        ingredient_id,
                        liqueur.get('amount', 0),
                        liqueur.get('unit', {'en': 'oz', 'zh': '盎司'})
                    )

            # Process other ingredients
            for ingredient in cocktail_data.get('ingredients', []):
                ingredient_id = self._get_or_create_ingredient(
                    ingredient['name']['en'],
                    ingredient['name']['zh'],
                    'ingredient'
                )
                if ingredient_id:
                    self._upsert_cocktail_ingredient(
                        cocktail_id,
                        ingredient_id,
                        ingredient.get('amount', 0),
                        ingredient.get('unit', {'en': 'oz', 'zh': '盎司'})
                    )

        except Exception as e:
            print(f"Error handling cocktail ingredients: {str(e)}")

    def _upsert_cocktail_ingredient(self, cocktail_id: str, ingredient_id: str, amount: float, unit: Dict) -> None:
        """Upsert a cocktail ingredient relationship"""
        try:
            # Get or create unit
            unit_id = self._get_or_create_unit(unit['en'], unit['zh'])
            if not unit_id:
                return

            # Prepare the relationship data
            relationship_data = {
                'cocktail_id': cocktail_id,
                'ingredient_id': ingredient_id,
                'unit_id': unit_id,
                'amount': amount
            }

            # Upsert the relationship
            self.client.table('cocktail_ingredients').upsert(relationship_data).execute()

        except Exception as e:
            print(f"Error upserting cocktail ingredient relationship: {str(e)}") 