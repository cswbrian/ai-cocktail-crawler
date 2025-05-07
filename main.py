import os
from workflow import CocktailWorkflow
from dotenv import load_dotenv

if __name__ == '__main__':
    # Load environment variables
    load_dotenv()
    
    # Verify Supabase configuration
    if not os.getenv("SUPABASE_URL") or not os.getenv("SUPABASE_KEY"):
        print("Error: SUPABASE_URL and SUPABASE_KEY environment variables must be set")
        print("Please create a .env file with these variables or set them in your environment")
        exit(1)
    
    # Initialize the workflow
    workflow = CocktailWorkflow()
    
    # Add your new cocktails here
    new_cocktails = [
        "Deshler",
        "Opera",
        "Dubonnet Cocktail",
        "Larchmont",
        "Honeymoon",
        "Golden Fizz"
        "Silver Fizz"
        "Royal Fizz",
        "Berlin Station Chief",
        "Starting Over",
        "Repose 1912",
        "Coffee Cocktail",
        # Add more cocktails here, one per line
    ]
    
    print(f"Processing {len(new_cocktails)} cocktails:")
    for cocktail in new_cocktails:
        print(f"- {cocktail}")
    
    # Run the workflow with standardization
    workflow.run_workflow(new_cocktails, standardize=True)
    
    print(f"\nTo add more cocktails, you can:")
    print("1. Add more cocktail names to the 'new_cocktails' list in this file")
    print("2. Or create new files in data/original/ with the cocktail data")
    print("3. Or run workflow.py directly to process all cocktails in data/original/")
