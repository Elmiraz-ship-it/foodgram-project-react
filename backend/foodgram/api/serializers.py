from rest_framework import serializers

from recipes.models import Tag, Ingredient, Recipe

class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'


class RecipeShoppingCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ['id', 'name', 'cooking_time']


class RecipeIngredientsSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    amount = serializers.IntegerField()


class RecipeTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id']


class CreateRecipeSerializer(serializers.Serializer):
    ingredients = RecipeIngredientsSerializer(many=True)
    tags = serializers.ListField()
    image = serializers.ImageField(required=False)
    name = serializers.CharField()
    text = serializers.CharField()
    cooking_time = serializers.IntegerField()

    def save(self, **kwargs):
        data = self.validated_data
        author = kwargs.get('author')
        if author is None:
            print('Нет автора')
            return
        ingredients = data['ingredients']
        name = data['name']
        text = data['text']
        cooking_time = data['cooking_time']
        tags = [Tag.objects.get(pk=id) for id in data['tags']]
        new = Recipe(
            name=name,
            text=text,
            cooking_time=cooking_time,
            author=author
        )
        new.save()
        for tag in tags:
            new.tags.add(tag)
        for item in ingredients:
            ingr = Ingredient.objects.get(id=item['id'])
            amount = item['amount']
            new.add_ingredient(ingr, amount)
