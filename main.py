import os
from workflow import CocktailWorkflow
from config import load_environment

if __name__ == '__main__':
    try:
        # Set environment to development by default if not set
        if not os.getenv("ENVIRONMENT"):
            os.environ["ENVIRONMENT"] = "development"
            print(f"Environment set to: {os.getenv('ENVIRONMENT')}")
        
        # Load environment variables
        load_environment()
        
        # Initialize the workflow
        workflow = CocktailWorkflow()
        
        # Add your new cocktails here
        new_cocktails = [
            "Old Fashioned",  # Adding a test cocktail
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
    
    except Exception as e:
        print(f"Error: {str(e)}")
        exit(1)
