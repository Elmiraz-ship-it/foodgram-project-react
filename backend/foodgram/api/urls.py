from django.urls import path
from api.views import RecipeApiView, TagApiView, IngredientApiView, FavouriteAPIView, ShoppingCartAPIView


urlpatterns = [
    path('recipes/', RecipeApiView.as_view()),
    path('recipes/<int:pk>/', RecipeApiView.as_view()),
    path('recipes/shopping_cart/download/', ShoppingCartAPIView.as_view()),
    path('recipes/<int:pk>/favourite/', FavouriteAPIView.as_view()),
    path('recipes/<int:pk>/shopping_cart/', ShoppingCartAPIView.as_view()),
    path('tags/', TagApiView.as_view()),
    path('tags/<int:pk>/', TagApiView.as_view()),
    path('ingredients/', IngredientApiView.as_view()),
    path('ingredients/<int:pk>/', IngredientApiView.as_view()),
]
    
