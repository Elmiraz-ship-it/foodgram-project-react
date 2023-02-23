from django.contrib import admin

from recipes.models import Ingredient, IngredientToRecipe, Recipe, Tag


class IngredientRecipeInline(admin.StackedInline):
    model = IngredientToRecipe
    min_num = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = (IngredientRecipeInline,)


# admin.site.register(Recipe)
admin.site.register(Tag)
admin.site.register(Ingredient)
admin.site.register(IngredientToRecipe)
