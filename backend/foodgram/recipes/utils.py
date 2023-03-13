from recipes.models import Ingredient, Recipe, IngredientToRecipe


def add_ingredient(recipe: Recipe, ingr: Ingredient, amount: int) -> None:
    new = IngredientToRecipe(recipe=recipe, ingredient=ingr, amount=amount)
    new.save()


def get_ingredients(recipe: Recipe) -> dict:
    ingredients = {}
    for i in recipe.to_recipe.all():
        ingredients[i.ingredient.name] = i.amount
    return ingredients
