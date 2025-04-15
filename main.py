from workflow import CocktailWorkflow

if __name__ == '__main__':
    # Initialize the workflow
    workflow = CocktailWorkflow()
    
    # Add your new cocktails here
    new_cocktails = [
        "French Kiss",
        "Mojito",
        "Margarita",
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
