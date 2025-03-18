from google import genai
from config import API_KEY
from pydantic import BaseModel
import json
from typing import List, Optional

class BilingualText(BaseModel):
    en: str
    zh: str
    

class Ingredient(BaseModel):
    amount: int
    name: BilingualText
    unit: BilingualText
    rationale: BilingualText
    

class FlavorProfile(BaseModel):
    sweetness: int
    sourness: int
    booziness: int
    body: int
    complexity: int
    bubbles: bool
    

class CocktailInfo(BaseModel):
    name: BilingualText
    description: BilingualText
    historical_reference: BilingualText
    technique: BilingualText
    garnish: BilingualText
    serve_in_glass: BilingualText
    appearance: BilingualText
    allergens: list[BilingualText]
    base_spirits: list[Ingredient]
    liqueurs: list[Ingredient]
    ingredients: list[Ingredient]
    flavor_descriptors: list[BilingualText]
    flavor_profile: FlavorProfile

class LLMClient:
    def __init__(self):
        self.client = genai.Client(api_key=API_KEY)
    
    def get_cocktail_info(self, cocktail_name: str) -> CocktailInfo | None:
        try:
            prompt = f"""You are a professional mixologist specializing in classic cocktails. Provide detailed information about {cocktail_name} in JSON format, and *only* in JSON format, adhering to the following rules:

1. Response MUST be valid JSON and ONLY JSON
2. Include all requested details
3. Verify measurements and techniques
4. Adhere strictly to required fields
5. Use generic names for all components
6. For all string fields, provide bilingual responses in both English (en) and Traditional Chinese Taiwan (zh) in the format: {{"en": "English text", "zh": "繁體中文"}}
7. For historical_reference and description fields, format the content as markdown text with proper formatting (e.g., **bold**, *italic*, bullet points)
8. For flavor_descriptors, only use from this exact list of accepted values:
   - Bitter (苦味)
   - Salty (有鹽)
   - Umami (鮮味)
   - Fruity (果香)
   - Citrus (柑橘)
   - Herbal (草本)
   - Spicy (辛辣)
   - Floral (花香)
   - Tropical (熱帶)
   - Nutty (堅果)
   - Chocolate (朱古力)
   - Coffee (咖啡)
   - Vanilla (香草)
   - Smoky (煙燻)
   - Earth (泥土)
   - Savory (鮮味)
   - Creamy (乳脂)
   - Woody (木質)
   - Grassy (草青)
   - Yeasty (酵母)

Example format:
{{
"name": {{"en": "Sazerac", "zh": "薩澤拉克"}},
"serve_in_glass": {{"en": "Chilled old-fashioned glass", "zh": "冰鎮古典杯"}},
"appearance": {{"en": "Clear amber liquid with a golden hue, no garnish", "zh": "清澈的琥珀色液體，帶有金黃色調，無裝飾"}},
"base_spirits": [
{{
"name": {{"en": "Rye Whisky", "zh": "黑麥威士忌"}},
"amount": 45,
"unit": {{"en": "ml", "zh": "毫升"}},
"rationale": {{"en": "Provides the cocktail's backbone...", "zh": "作為調酒的基酒..."}}
}}
],
"ingredients": [
{{
"name": {{"en": "Sugar Cube", "zh": "方糖"}},
"amount": 1,
"unit": {{"en": "pc", "zh": "個"}},
"rationale": {{"en": "Adds subtle sweetness...", "zh": "增添微妙甜味..."}}
}}
],
"liqueurs": [],
"technique": {{"en": "Rinse chilled glass with absinthe...", "zh": "用苦艾酒沖洗冰鎮過的杯子..."}},
"garnish": {{"en": "Lemon peel twist (discarded)", "zh": "檸檬皮扭花（使用後丟棄）"}},
"flavor_profile": {{
"sweetness": 4,
"sourness": 1,
"booziness": 8,
"body": 6,
"complexity": 9,
"bubbles": false
}},
"historical_reference": {{
    "en": "**Origin**: First documented in Harry Craddock's *Savoy Cocktail Book* (1930)\\n\\n* Created in New Orleans in the 1850s\\n* Named after Sazerac de Forge et Fils cognac\\n* Originally made with cognac before switching to rye whiskey",
    "zh": "**起源**: 首次記載於哈利·克拉多克的《*薩伏伊雞尾酒書*》（1930年）\\n\\n* 1850年代在紐奧良創製\\n* 以Sazerac de Forge et Fils干邑白蘭地命名\\n* 最初使用干邑調製，後改用黑麥威士忌"
}},
"description": {{
    "en": "**Classic New Orleans Cocktail**\\n\\nA sophisticated blend of rye whiskey and bitters, featuring:\\n* Absinthe rinse for aromatic complexity\\n* Sugar cube for balanced sweetness\\n* Peychaud's bitters for distinctive flavor",
    "zh": "**經典紐奧良雞尾酒**\\n\\n黑麥威士忌與苦精的精緻調和，特色：\\n* 苦艾酒杯潤增添香氣層次\\n* 方糖帶來均衡甜度\\n* Peychaud's苦精營造獨特風味"
}},
"allergens": [{{"en": "egg white", "zh": "蛋白"}}],
"flavor_descriptors": [
    {{"en": "Herbal", "zh": "草本"}},
    {{"en": "Spicy", "zh": "辛辣"}},
    {{"en": "Bitter", "zh": "苦味"}},
    {{"en": "Smoky", "zh": "煙燻"}}
]
}}

Provide information for {cocktail_name} in this exact JSON format."""
            
            response = self.client.models.generate_content(
                model='gemini-2.0-flash',
                contents=prompt,
                config={ 
                'response_mime_type': 'application/json',
                'response_schema': CocktailInfo, 
                }, 
            )
            
            # Print the raw response
            print("Raw Response:", response.text)
            
            # Parse the JSON response and create CocktailInfo object
            data = response.parsed
            return data  # Just return the parsed object directly
        except Exception as e:
            print(f"Error processing {cocktail_name}: {str(e)}")
            return None

