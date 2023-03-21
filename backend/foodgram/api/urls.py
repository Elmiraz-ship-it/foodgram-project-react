from api.views import (FavouriteAPIView, IngredientApiView, RecipeApiView,
                       ShoppingCartAPIView, SubscribeAPIView, TagApiView)
from django.urls import include, path

urlpatterns = [
    path('recipes/', RecipeApiView.as_view()),
    path('recipes/<int:pk>/', RecipeApiView.as_view()),
    # path('recipes/test/', RecipeApiView.as_view()),
    path('recipes/download_shopping_cart/', ShoppingCartAPIView.as_view()),
    path('recipes/<int:pk>/favorite/', FavouriteAPIView.as_view()),
    path('favorites/', FavouriteAPIView.as_view()),
    path('recipes/<int:pk>/shopping_cart/', ShoppingCartAPIView.as_view()),
    path('tags/', TagApiView.as_view()),
    path('tags/<int:pk>/', TagApiView.as_view()),
    path('ingredients/', IngredientApiView.as_view()),
    path('ingredients/<int:pk>/', IngredientApiView.as_view()),
    path('users/subscriptions/', SubscribeAPIView.as_view()),
    path('auth/', include('djoser.urls.authtoken')),
    path('', include('djoser.urls')),
    path('users/<int:pk>/subscribe/', SubscribeAPIView.as_view())
]
