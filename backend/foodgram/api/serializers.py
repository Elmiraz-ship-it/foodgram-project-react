from typing import List

from rest_framework import serializers

from recipes.models import Tag, Ingredient, Recipe, IngredientToRecipe
from users.models import Follow, CustomUser


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


class CreateRecipeSerializer(serializers.ModelSerializer):
    ingredients = RecipeIngredientsSerializer(many=True)

    def create(self, validated_data, **kwargs):
        author = kwargs.get('author')
        ingredients = validated_data.get('ingredients')
        if not ingredients:
            return False
        name = validated_data['name']
        text = validated_data['text']
        cooking_time = validated_data['cooking_time']
        tags = [Tag.objects.get(pk=id) for id in validated_data['tags']]
        new = Recipe(
            name=name,
            text=text,
            cooking_time=cooking_time,
            author=author
        )
        new.save()
        to_create = []
        for tag in tags:
            new.tags.add(tag)
        for item in ingredients:
            ingr = Ingredient.objects.get(id=item['id'])
            amount = item['amount']
            to_create.append(IngredientToRecipe(
                    recipe=new,
                    ingredient=ingr,
                    amount=amount
                )
            )
        IngredientToRecipe.objects.bulk_create(to_create)
        return new


class FollowRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ['id', 'name', 'cooking_time', 'image']

class FollowSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='author.email')
    id = serializers.IntegerField(source='author.id')
    username = serializers.CharField(source='author.username')
    first_name = serializers.CharField(source='author.first_name')
    last_name = serializers.CharField(source='author.last_name')
    is_subscribed = serializers.SerializerMethodField()
    recipes = FollowRecipeSerializer(source='author.recipes', many=True)
    recipes_count = serializers.SerializerMethodField()
    
    def get_recipes_count(self, obj: Follow):
        return obj.author.recipes.count()
    
    @staticmethod
    def get_subscribes_on(user: CustomUser) -> List[CustomUser]:
        subs = [f.author for f in user.follower.all().select_related('author')]
        return subs
    
    def get_is_subscribed(self, obj: Follow):
        current_user = obj.user
        return current_user in self.get_subscribes_on(obj.author)
    

    class Meta:
        model = Follow
        fields = [
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count'
        ]
