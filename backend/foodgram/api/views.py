import os
import tempfile

from api.serializers import (CreateRecipeSerializer, FavouriteRecipeSerializer,
                             FollowSerializer, IngredientSerializer,
                             RecipeSerializer, RecipeShoppingCartSerializer,
                             TagSerializer)
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
    is_favorited = filters.BooleanFilter(method='filter_is_favourited')
    is_in_shopping_cart = filters.BooleanFilter(
        method='filter_is_in_shopping_cart'
    )

    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all()
    )

    def filter_is_favourited(self, queryset, name, value):
        user = self.request.user
        if value and not user.is_anonymous:
            return self.request.user.favourite.all()
        return queryset

    def filter_is_in_shopping_cart(self, queryset, name, value):
        user = self.request.user
        if value and not user.is_anonymous:
            return self.request.user.shopping_cart.all()
        return queryset

    class Meta:
        model = Recipe
        fields = ['tags', 'author']


class RecipeApiView(ListCreateAPIView, UpdateAPIView, DestroyAPIView):
    http_method_names = ['get', 'post', 'patch', 'delete']
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = RecipeFilterSet

    def get_queryset(self):
        return Recipe.objects.all()

    def get_serializer_class(self):
        serializers = {
            'GET': RecipeSerializer,
            'POST': CreateRecipeSerializer,
            'PATCH': CreateRecipeSerializer
        }
        return serializers[self.request.method]

    def get(self, request, pk=None):
        if pk is not None:
            recipe = get_object_or_404(Recipe, id=pk)
            serializer = self.get_serializer_class()(
                recipe, context={'request': request}
            )
            return Response(serializer.data)

        if request.GET.get('is_favorited') in ('1', 'true'):
            if request.GET.get('tags') is None:
                return super().get(request)

            qs = request.user.favourite.filter(
                tags__slug__in=request.GET.getlist('tags')
            )

            serializer = self.get_serializer_class()(
                qs, context={'request': request}, many=True
            )
            result_page = self.paginator.paginate_queryset(qs, request)
            serializer = self.get_serializer_class()(
                result_page, many=True, context={'request': request}
            )
            return self.paginator.get_paginated_response(serializer.data)
        return super().get(request)

    def post(self, request):
        serializer = self.get_serializer_class()(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['author'] = request.user
        new = serializer.save()
        response = RecipeSerializer(new, context={'request': request})
        return Response(status=status.HTTP_201_CREATED, data=response.data)


class TagApiView(ListAPIView):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    pagination_class = None

    def get(self, request, pk=None):
        if pk is not None:
            tag = get_object_or_404(Tag, id=pk)
            serializer = self.serializer_class(
                tag, context={'request': request}
            )
            return Response(serializer.data)
        return super().get(request)


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
    pagination_class = None

    def get(self, request, pk=None):
        if pk is not None:
            ingr = get_object_or_404(Ingredient, id=pk)
            serializer = self.serializer_class(
                ingr, context={'request': request}
            )
            return Response(serializer.data)
        return super().get(request)


class FavouriteAPIView(ListAPIView):
    serializer_class = RecipeSerializer
    pagination_class = None

    def get_queryset(self):
        return self.request.user.favourite.all()

    def post(self, request, pk=None):
        if pk is not None:
            recipe = get_object_or_404(Recipe, id=pk)
            if recipe in request.user.favourite.all():
                return Response(
                    status=status.HTTP_400_BAD_REQUEST,
                    data={"errors": "рецепт уже есть в избранном"}
                )
            request.user.favourite.add(recipe)
            serializer = FavouriteRecipeSerializer(recipe)
            return Response(
                status=status.HTTP_201_CREATED, data=serializer.data
            )
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
