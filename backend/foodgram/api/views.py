import os
import tempfile

from api.serializers import (CreateRecipeSerializer, FollowSerializer,
                             IngredientSerializer, RecipeSerializer,
                             RecipeShoppingCartSerializer, TagSerializer)
from api.utils import get_file_payload
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from django_filters import rest_framework as filters
from recipes.models import Ingredient, Recipe, Tag
from rest_framework import status
from rest_framework.generics import (DestroyAPIView, ListAPIView,
                                     ListCreateAPIView, UpdateAPIView)
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from users.models import CustomUser, Follow
from users.utils import new_follow, unsubscribe_user_from


class RecipeFilterSet(filters.FilterSet):
    tags = filters.AllValuesMultipleFilter(
        field_name='tags__slug', lookup_expr='contains'
    )
    is_favourited = filters.BooleanFilter(method='filter_is_favourited')
    is_in_shopping_cart = filters.BooleanFilter(
        method='filter_is_in_shopping_cart'
    )

    def filter_is_favourited(self, queryset, name, value):
        if value and not self.request.user.is_anonymous:
            pass
        return queryset

    def filter_is_shopping_cart(self, queryset, name, value):
        if value and not self.request.user.is_anonymous:
            pass
        return queryset

    class Meta:
        model = Recipe
        fields = ['tags', 'author']


class RecipeApiView(ListCreateAPIView, UpdateAPIView, DestroyAPIView):
    serializer_class = RecipeSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = RecipeFilterSet

    def get_queryset(self):
        return Recipe.objects.all()

    def post(self, request):
        serializer = CreateRecipeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['author'] = request.user
        serializer.save()
        return Response()


class TagApiView(ListAPIView):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()


class IngredientsFilterSet(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')

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
                with tempfile.NamedTemporaryFile(delete=False, mode='w') as f:
                    for key, value in data.items():
                        f.write(f'{key}\n')
                        for k, v in value.items():
                            f.write(f'{k} {v}\n')
                response = FileResponse(
                    open(f.name, 'rb'),
                    as_attachment=True,
                    filename=filename
                )
                return response
            finally:
                os.remove(f.name)
        return Response(status=status.HTTP_200_OK)

    def post(self, request, pk=None):
        if pk is not None:
            recipe = get_object_or_404(Recipe, id=pk)
            request.user.shopping_cart.add(recipe)
            serializer = RecipeShoppingCartSerializer(recipe)
            return Response(
                data=serializer.data, status=status.HTTP_201_CREATED
            )
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
                return Response(
                    serializer.data, status=status.HTTP_201_CREATED
                )
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        if pk is not None:
            author = get_object_or_404(CustomUser, id=pk)
            result = unsubscribe_user_from(request.user, author)
            return Response(status=status.HTTP_204_NO_CONTENT)
        if not result:
            return Response(status=status.HTTP_400_BAD_REQUEST)
