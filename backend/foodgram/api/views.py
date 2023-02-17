from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, ListAPIView
from rest_framework.views import APIView
from django_filters import rest_framework as filters
from django.shortcuts import get_object_or_404
from api.utils.to_csv import data_to_csv

from recipes.models import Recipe, Tag, Ingredient
from api.serializers import RecipeSerializer, TagSerializer, IngredientSerializer, CreateRecipeSerializer, RecipeShoppingCartSerializer


class RecipeApiView(ListCreateAPIView):
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()

    def post(self, request):
        serializer = CreateRecipeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=request.user)
        return Response(serializer.validated_data)


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


class FavouriteAPIView(APIView):
    def post(self, request, pk=None):
        if pk is not None:
            recipe = get_object_or_404(Recipe, id=pk)
            request.user.favourite.add(recipe)
            return Response(status=201)
        return Response(status=404)

    def delete(self, request, pk=None):
        if pk is not None:
            recipe = get_object_or_404(Recipe, id=pk)
            request.user.favourite.remove(recipe)
            return Response(status=204)
        return Response(status=404)


class ShoppingCartAPIView(APIView):
    def get(self, request):
        shopping_cart = request.user.shopping_cart.values()
        data_to_csv(shopping_cart, 'shopping_cart.csv')
        return Response(status=200)

    def post(self, request, pk=None):
        if pk is not None:
            recipe = get_object_or_404(Recipe, id=pk)
            request.user.shopping_cart.add(recipe)
            serializer = RecipeShoppingCartSerializer(recipe)
            return Response(data=serializer.data, status=201)
        return Response(status=404)

    def delete(self, request, pk=None):
        if pk is not None:
            recipe = get_object_or_404(Recipe, id=pk)
            request.user.shopping_cart.remove(recipe)
            return Response(status=204)
        return Response(status=404)
