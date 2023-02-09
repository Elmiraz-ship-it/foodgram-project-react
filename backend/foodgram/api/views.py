from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, ListAPIView
from django_filters import rest_framework as filters

from recipes.models import Recipe, Tag, Ingredient
from api.serializers import RecipeSerializer, TagSerializer, IngredientSerializer


class RecipeApiView(ListCreateAPIView):
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()


class TagApiView(ListAPIView):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()


class IngredientsFilterSet(filters.FilterSet):
    name = filters.CharFilter(field_name='title', lookup_expr='icontains')
    class Meta:
        model = Ingredient
        fields = '__all__'


class IngredientApiView(ListAPIView):
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = IngredientsFilterSet
