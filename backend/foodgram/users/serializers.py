from rest_framework import serializers


from recipes.models import Recipe
from users.models import Follow

class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ['id', 'name', 'cooking_time']

class FollowSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='author.email')
    id = serializers.IntegerField(source='author.id')
    username = serializers.CharField(source='author.username')
    first_name = serializers.CharField(source='author.first_name')
    last_name = serializers.CharField(source='author.last_name')
    is_subscribed = serializers.SerializerMethodField()
    recipes = RecipeSerializer(source='author.recipes', many=True)
    recipes_count = serializers.SerializerMethodField()
    
    def get_recipes_count(self, obj):
        return obj.author.recipes.count()

    def get_is_subscribed(self, obj):
        current_user = obj.user
        return current_user in obj.author.get_subscribes_on()

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
