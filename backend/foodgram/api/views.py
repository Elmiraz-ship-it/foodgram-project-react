from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, ListAPIView
from rest_framework.views import APIView
from django_filters import rest_framework as filters
from django.shortcuts import get_object_or_404

from recipes.models import Recipe, Tag, Ingredient
from api.serializers import RecipeSerializer, TagSerializer, IngredientSerializer, CreateRecipeSerializer


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
