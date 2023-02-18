from django.conf import settings
from django.core.management.base import BaseCommand
from recipes.models import Ingredient

import json

class Command(BaseCommand):
    def load_to_db(self, data):
        to_create = []
        for item in data:
            to_create.append(Ingredient(**item))
            print('ingredient', item['name'], 'created')
        Ingredient.objects.bulk_create(to_create)

    def handle(self, *args, **options):
        filename = f'{settings.BASE_DIR}/../../data/ingredients.json'
        try:
            with open(filename, encoding='utf-8') as json_file:
                data = json.load(json_file)
                self.load_to_db(data)
        except FileNotFoundError:
            msg = "Убедитесь, что в папке data есть файл ingredients.json"
            self.stdout.write(self.style.ERROR(msg))
        except json.JSONDecodeError:
            msg = "Убедитесь, что файл формата json"
            self.stdout.write(self.style.ERROR(msg))