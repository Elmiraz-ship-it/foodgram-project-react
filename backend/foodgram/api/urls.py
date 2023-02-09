from django.urls import path
from api.views import RecipeApiView, TagApiView, IngredientApiView


urlpatterns = [
    path('recipes/', RecipeApiView.as_view()),
    path('recipes/<int:pk>/', RecipeApiView.as_view()),
    path('tags/', TagApiView.as_view()),
    path('tags/<int:pk>/', TagApiView.as_view()),
    path('ingredients/', IngredientApiView.as_view()),
    path('ingredients/<int:pk>/', IngredientApiView.as_view()),
]
    
