from llm_client import LLMClient
import json
import os

# Create data/cocktails directory if it doesn't exist
os.makedirs('data/cocktails', exist_ok=True)

cocktails = [
    "Sazerac", "Mojito" ,"Virgin Mojito", "Vieux Carré", "Alexender", "Tequila Sunrise", "Old Fashioned", "Negroni", "Widow's Kiss", "Old Cuban", "Daiquiri", "Dry Martini", "Margarita", "Manhattan", "Whiskey Sour", "Espresso Martini", "Aperol Spritz", "Moscow Mule", "Cosmopolitan", "Mai Tai", "Pina Colada", "Bloody Mary", "Long Island Iced Tea", "Singapore Sling", "Caipirinha", "Bellini", "Last Word", "Diamondback", "Bijou", "Greenpoint", "La Louisiane", "Mezcal Margarita", "Smoky Paloma", "Scotch Sour", "Penicillin", "Rob Roy", "Blood & Sand", "Islay Mist", "Rusty Nail", "Boulevardier", "Godfather", "Revolving Door", "Last of the Mohicans", "Gunsmoke", "Campfire Cocktail", "Smoked Maple Old Fashioned", "Bacon Bourbon Manhattan", "Smoked Pineapple Margarita", "Chipotle Bloody Mary", "Mezcal Negroni", "Smoked Rosemary Gimlet", "Lapsang Souchong Martini", "Smoked Peach Bellini", "Smoked Fig and Bourbon Sour", "Charred Orange Paloma", "Smoked Vanilla Espresso Martini", "Martini", "Mimosa", "French 75", "Sidecar", "Amaretto Sour", "Pisco Sour", "Tom Collins", "Gin Fizz", "Dark 'n' Stormy", "White Russian", "Black Russian", "Grasshopper", "Paloma", "Campari Spritz", "Americano", "Negroni Sbagliato", "Bamboo Cocktail", "Bee's Knees", "Between the Sheets", "Bramble", "Corpse Reviver No. 2", "Clover Club", "Death in the Afternoon", "Derby", "El Diablo", "Flip", "French Connection", "Gimlet", "Hanky Panky", "Harvey Wallbanger", "Horse's Neck", "Irish Coffee", "Jack Rose", "Japanese Slipper", "Kir Royale", "Mint Julep", "Monkey Gland", "Old Pal", "Paper Plane", "Perfect Manhattan", "Planter's Punch", "Queen's Park Swizzle", "Ramos Gin Fizz", "Scofflaw", "Sherry Cobbler", "Sloe Gin Fizz", "Smash", "Southside", "Stinger", "Suffering Bastard", "The Last Word", "Three-Mile Long Island Iced Tea", "Ti' Punch", "Tom and Jerry", "Trinidad Sour", "Tuxedo", "Vesper", "Ward Eight", "Whiskey Smash", "White Lady", "Zombie", "Aviation", "Pimm's Cup", "Corpse reviver #2", "Chrysanthemum", "Black and tan", "Black velvet", "Boilermaker", "Hangman's blood", "Irish car bomb", "Michelada", "Monaco", "Porchcrawler", "Queen Mary", "Sake bomb", "Shandy", "Snakebite", "Spaghett", "U-boot", "Angel face", "Blow my skull", "Brandy Alexander", "Brandy crusta", "Brandy old fashioned", "Brandy Manhattan", "Brandy sour", "Chicago cocktail", "Curaçao punch", "Diki-diki", "Four score", "Hennchata", "Hoppel poppel", "Incredible Hulk", "Paradise", "Porto flip", "Savoy affair", "Savoy corpse reviver", "The Blenheim", "Batida", "Caju amigo", "Leite de onça", "Quentão", "Rabo-de-galo", "20th century", "Blackthorn", "Bloody Margaret", "Breakfast martini", "Bronx", "Casino", "Cloister", "Clover Club cocktail", "Cooperstown cocktail", "Damn the weather", "Fluffy duck", "Gibson", "Gin and tonic", "Gin pahit", "Gin sour", "Greyhound", "John Collins", "Lime Rickey", "Lorraine", "Martinez", "Moon River", "My Fair Lady", "Old Etonian", "Pegu club", "Pink gin", "Pink lady", "Queens", "Royal arrival", "Salty dog", "Takumi's aviation", "Delilah", "Wolfram", "Ancient Mariner", "Airmail", "Bacardi", "Barracuda", "Blue Hawaii", "Blue Hawaiian", "Bumbo", "Bushwacker", "Cobra's fang", "Cojito", "Cremat", "Cuban sunset", "El Presidente", "Fish house punch", "Flaming Doctor Pepper", "Flaming volcano", "Fluffy critter", "Grog", "Gunfire", "Hot buttered rum", "Hurricane", "Jagertee", "Macuá", "Mary Pickford", "Mr. Bali Hai", "Painkiller", "Piña colada", "Q.B. Cooler", "Royal Bermuda", "Cuba libre", "Rum swizzle", "Sumatra Kula", "Test pilot", "Trumptini", "Tschunk", "Yellow bird", "Saketini", "Tamagozake", "Boston tea party", "Batanga", "Bloody Maria", "Cantarito", "Chimayó cocktail", "Death Flip", "Harlem mugger", "Juan Collins", "Matador", "Mexican firing squad", "Mexican martini", "Mojito blanco", "Sangrita", "Tequila & Tonic", "Tequila slammer", "Tequila sour", "Tommy's margarita", "Vampiro", "Illegal", "Naked and famous", "Oaxaca old fashioned", "Mezcal last word", "Tia mia", "Division bell", "Medicina Latina", "Appletini", "Astro pop", "Bay breeze", "BLT cocktail", "Blue Lagoon", "Bull shot", "Caesar", "Caipiroska", "Cape Codder", "Chi-chi", "Colombia", "Dirty Shirley", "Flirtini", "Glowtini", "Godmother", "John Daly", "Kamikaze", "Karsk", "Kensington Court special", "Lemon drop", "Link up", "Orange tundra", "Platinum blonde", "Porn star martini", "Red Russian", "Rose Kennedy cocktail", "Screwdriver", "Sea breeze", "Sex on the beach", "Spicy Fifty", "Vargtass", "Vodka gimlet", "Kangaroo", "Vodka McGovern", "Woo woo", "Wściekły pies", "Yorsh", "Amber moon", "Black nail", "Blood and Sand", "Blue blazer", "Bobby Burns", "Bourbon lancer", "Brooklyn", 
    "Churchill", "Farnell", "Horsefeather", "Whiskey and Coke", "Lynchburg lemonade", "Missouri mule", "New York sour", "Nixon", "Scotch and soda", "Seven and Seven", "Three wise men", "Toronto", "Ward 8", "Whisky Mac", "Cheeky Vimto", "Portbuka", "Rebujito", "Up to date", "Rose", "Adonis", "Agua de Valencia", "Prince of Wales", "Agua de Sevilla", "Spritz", "Hugo", "Rossini", "Atomic", "Chambord Royale", "Champagne cocktail", "Kir royal", "Ochsenblut", "Calimocho or Kalimotxo", "Claret cup", "Glögg", "Tinto de verano", "Zurracapote", "Kir", "Spritzer", "Chocolate martini", "Herbsaint frappé", "Mauresque", "Perroquet", "Rourou", "Tomate", "B-52", "Baby Guinness", "Moose milk", "Orgasm", "Cement mixer", "Oatmeal cookie", "Quick fuck", "Slippery nipple", "Springbokkie", "Revelation", 
    "Aguaymanto sour", "Jazmin sour", "Mango sour", "Piscola", "Fuzzy navel", "Polar bear", "Redheaded slut", "Brut cocktail", "Fernet con coca", "Alabama slammer", "Blueberry tea"
    "Mudslide", "Dirty Martini", "Gibson", "Bloody Mary", "Caesar", "Michelada", "Bull Shot", "Salty Dog", "Oyster Shooter", "Pickleback", "Red Snapper", "Vesper", "Manhattan", "Rob Roy", "Sazerac", "Old Pal", "Boulevardier", "Negroni", "Americano", "Campari Spritz", "Cynar Spritz", "Averna Spritz", "Fernet Branca & Coke", "Black Velvet", "Irish Coffee", "French 75", "Last Word", "Paper Plane", "Gold Rush", "Bees Knees", "Sidecar", "Margarita", "Paloma", "Tommy's Margarita", "Ranch Water", "El Diablo", "Moscow Mule", "Dark 'n' Stormy", "Mai Tai", "Painkiller", "Zombie", "Singapore Sling", "Pisco Sour", "Clover Club", "Bramble", "Aviation", "Penicillin", "Chartreuse Swizzle", "Trinidad Sour", "Espresso Martini", "Last Word", "Bijou", "Clover Club", "French 75", "Gimlet", "Hanky Panky", "Hemingway Daiquiri", "Jungle Bird", "Mai Tai", "Margarita", "Mojito", "Moscow Mule", "Negroni", "Old Pal", "Paloma", "Pimm's Cup", "Planter's Punch", "Sazerac", "Sidecar", "Singapore Sling", "Stinger", "Tom Collins", "Vieux Carré", "White Lady", "Zombie", "Aviation", "Bramble", "Chartreuse Swizzle", "Daisy de Santiago", "Derby", "El Diablo", "Fitzgerald", "Floradora", "Green Beast", "Irish Maid", "Jasmine", "Kentucky Buck", "Lion's Tail", "Martinez", "Mint Julep", "Oaxaca Old Fashioned", "Penicillin", "Queen's Park Swizzle", "Remember the Maine", "Scofflaw", "Ti' Punch", "Toronto", "Ward Eight", "Tipperary", "Gypsy", "Nuclear daiquiri", "Byculla", "Calvados port", "Purgatory", "12 mile limits", "Egg Nog", "Twelve Mile Limit", "Ciro's Special"
]

client = LLMClient()

async def fetchCocktails():
    cocktail_data_list = []
    
    for cocktail in cocktails:
        filePath = f"data/cocktails/{cocktail.lower().replace(' ', '_')}.json"
        
        # Check if file exists using Python's os.path
        if not os.path.exists(filePath):
            cocktail_info = await client.get_cocktail_info(cocktail)
            if cocktail_info:
                cocktail_data_list.append(cocktail_info)
        else:
            print(f"Skipping {cocktail}, file already exists.")

    return cocktail_data_list

for cocktail in cocktails:
    print(f"Processing {cocktail}...")
    filename = f"data/cocktails/{cocktail.lower().replace(' ', '_')}.json"
    
    # Add file existence check
    if not os.path.exists(filename):
        cocktail_info = client.get_cocktail_info(cocktail)
        
        if cocktail_info:
            # Convert to JSON and save to file
            with open(filename, 'w') as f:
                json.dump(cocktail_info.dict(), f, indent=2)
            print(f"Saved {cocktail} to {filename}")
        else:
            print(f"Failed to process {cocktail}")
    else:
        print(f"Skipping {cocktail}, file already exists.")
