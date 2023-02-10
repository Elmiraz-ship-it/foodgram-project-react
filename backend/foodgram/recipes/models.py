from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()

# Create your models here.
class Tag(models.Model):
    name = models.CharField(max_length=32)
    color = models.CharField(max_length=32)

    def __str__(self) -> str:
        return self.name
        

class Ingredient(models.Model):
    name = models.CharField(max_length=32)
    mesurement_unit = models.CharField(max_length=32)

    def __str__(self) -> str:
        return self.name


class IngredientToRecipe(models.Model):
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE, related_name='to_recipe')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, related_name='to_recipe')
    amount = models.IntegerField()


class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=32)
    text = models.TextField(max_length=512, null=True, blank=True)
    cooking_time = models.IntegerField(null=True, blank=True)
    tag = models.ManyToManyField(Tag)
    
    def add_ingredient(self, ingr, amount):
        new = IngredientToRecipe(recipe=self, ingredient=ingr, amount=amount)
        new.save()
    
    def get_ingredients(self):
        ingredients = {}
        for i in self.to_recipe.all():
            ingredients[i.ingredient.title] = i.amount
        return ingredients

    def __str__(self) -> str:
        return self.name
