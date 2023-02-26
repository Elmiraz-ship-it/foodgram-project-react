from recipes.models import Recipe
from recipes.utils import get_ingredients

def get_file_payload(data):
    payload = {}
    for item in data:
        recipe = Recipe.objects.get(id=item['id'])
        ingredients = get_ingredients(recipe)
        payload[recipe.name] = ingredients
    return payload        
