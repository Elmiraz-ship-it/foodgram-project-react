import os
import tempfile

from django.http import FileResponse
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
from api.utils import get_file_payload
from recipes.models import Ingredient, Recipe, Tag
from users.models import CustomUser, Follow
from users.utils import new_follow, unsubscribe_user_from


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
            data = get_file_payload(shopping_cart)
            filename = f'{request.user.username}_shopping_cart.txt'
            try:
                with tempfile.NamedTemporaryFile(delete=False, mode='w') as file:
                    for key, value in data.items():
                        file.write(f'{key}\n')
                        for k, v in value.items():
                            file.write(f'{k} {v}\n')
                response = FileResponse(
                    open(file.name, 'rb'),
                    as_attachment=True,
                    filename=filename
                )
                return response
            finally:
                os.remove(file.name)
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


class SubscribeAPIView(ListCreateAPIView, DestroyAPIView):
    pagination_class = LimitOffsetPagination
    serializer_class = FollowSerializer

    def get_queryset(self):
        return Follow.objects.filter(user=self.request.user)

    def post(self, request, pk=None):
        if pk is not None:
            author = get_object_or_404(CustomUser, id=pk)
            follow = new_follow(request.user, author)
            if follow is not None:
                serializer = FollowSerializer(follow)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        if pk is not None:
            author = get_object_or_404(CustomUser, id=pk)
            result = unsubscribe_user_from(request.user, author)
            return Response(status=status.HTTP_204_NO_CONTENT)
        if not result:
            return Response(status=status.HTTP_400_BAD_REQUEST)
