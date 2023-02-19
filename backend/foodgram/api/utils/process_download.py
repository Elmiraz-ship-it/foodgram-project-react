from django.conf import settings
from recipes.models import Recipe

def process_data(data):
    payload = {}
    for item in data:
        recipe = Recipe.objects.get(id=item['id'])
        ingredients = recipe.get_ingredients()
        payload[recipe.name] = ingredients
    return payload        

def to_download_shopping_cart(data, username):
    data = process_data(data)
    filename = username + '_shopping_cart.txt'
    path_to_file = f'{settings.BASE_DIR}\{filename}'
    with open(path_to_file, 'w', encoding='utf-8') as file:
        for key, value in data.items():
            file.write(f'{key}\n')
            for k, v in value.items():
                file.write(f'{k} {v}\n')
    return path_to_file

