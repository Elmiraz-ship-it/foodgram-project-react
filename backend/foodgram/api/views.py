from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, ListAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.views import APIView
from django_filters import rest_framework as filters
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from api.utils.process_download import to_download_shopping_cart

from recipes.models import Recipe, Tag, Ingredient
from api.serializers import RecipeSerializer, TagSerializer, IngredientSerializer, CreateRecipeSerializer, RecipeShoppingCartSerializer


class RecipeApiView(ListCreateAPIView, UpdateAPIView, DestroyAPIView):
    serializer_class = RecipeSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self):
        return Recipe.objects.filter(author=self.request.user)

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
        if shopping_cart:
            path_to_file = to_download_shopping_cart(shopping_cart, request.user.username)
            if path_to_file:
                filename = path_to_file.split('\\')[-1]
                with open(path_to_file, 'r', encoding='utf-8') as file:
                    response = HttpResponse(file, content_type='text/txt')
                    response['Content-Disposition'] = f'attachment; filename={filename}'
                    return response
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
