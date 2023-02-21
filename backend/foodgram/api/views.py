from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters import rest_framework as filters
from rest_framework import status
from rest_framework.generics import (
    DestroyAPIView,
    ListAPIView,
    ListCreateAPIView,
    UpdateAPIView
)
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import (
    CreateRecipeSerializer,
    FollowSerializer,
    IngredientSerializer,
    RecipeSerializer,
    RecipeShoppingCartSerializer,
    TagSerializer
)
from api.utils.process_download import to_download_shopping_cart
from recipes.models import Ingredient, Recipe, Tag
from users.models import CustomUser, Follow


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
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk=None):
        if pk is not None:
            recipe = get_object_or_404(Recipe, id=pk)
            request.user.favourite.remove(recipe)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)


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

        return Response(status=status.HTTP_200_OK)

    def post(self, request, pk=None):
        if pk is not None:
            recipe = get_object_or_404(Recipe, id=pk)
            request.user.shopping_cart.add(recipe)
            serializer = RecipeShoppingCartSerializer(recipe)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk=None):
        if pk is not None:
            recipe = get_object_or_404(Recipe, id=pk)
            request.user.shopping_cart.remove(recipe)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)


class SubscribeAPIView(ListAPIView):
    pagination_class = LimitOffsetPagination
    serializer_class = FollowSerializer

    def get_queryset(self):
        return Follow.objects.filter(user=self.request.user)

    def post(self, request, pk=None):
        if pk is not None:
            author = get_object_or_404(CustomUser, id=pk)
            new_follow = request.user.new_follow(author)
            if new_follow is not None:
                serializer = FollowSerializer(new_follow)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        if pk is not None:
            author = get_object_or_404(CustomUser, id=pk)
            result = request.user.unsubscribe_from(author)
            return Response(status=status.HTTP_204_NO_CONTENT)
        if not result:
            return Response(status=status.HTTP_400_BAD_REQUEST)
