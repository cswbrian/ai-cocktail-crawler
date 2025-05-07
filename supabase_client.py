import os
from supabase import create_client, Client
from typing import Dict, Optional

class SupabaseClient:
    def __init__(self):
        url = os.environ.get("SUPABASE_URL")
        key = os.environ.get("SUPABASE_KEY")
        if not url or not key:
            raise ValueError("SUPABASE_URL and SUPABASE_KEY environment variables must be set")
        self.client: Client = create_client(url, key)
    
    def upsert_cocktail(self, cocktail_data: Dict) -> Optional[Dict]:
        """
        Upsert a cocktail into the database using the slug as the unique identifier.
        Returns the updated/inserted record if successful, None if failed.
        """
        try:
            # Extract the slug from the cocktail data
            slug = cocktail_data.get('slug')
            if not slug:
                raise ValueError("Cocktail data must contain a slug")
            
            # Prepare the data for upsert
            data = {
                'slug': slug,
                'data': cocktail_data
            }
            
            # Perform the upsert operation with on_conflict parameter
            result = self.client.table('cocktails').upsert(
                data,
                on_conflict='slug'  # Specify the column to check for conflicts
            ).execute()
            
            if result.data:
                return result.data[0]
            return None
            
        except Exception as e:
            print(f"Error upserting cocktail: {str(e)}")
            return None 