from recipes.models import Recipe, Ingredient, Tag
from django.contrib.auth import get_user_model

def test_recipe():
    User = get_user_model()

    author = User.objects.get(email='admin@admin.com')
    tag = Tag.objects.get(title='завтрак')

    egg = Ingredient(title='яйцо', metric='шт')
    bacon = Ingredient(title='бекон', metric='гр')

    egg.save()
    bacon.save()

    new_recipe = Recipe(
        author=author,
        title='яичница с беконом',
        description='яичница с беконом',
        time_to_cook=5,
    )
    new_recipe.save()
    new_recipe.tag.add(tag)

    new_recipe.add_ingredient(egg, 2)
    new_recipe.add_ingredient(bacon, 100)
