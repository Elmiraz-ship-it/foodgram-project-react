from django.urls import include, path
from api.views import (
    IngredientApiView,
    FavouriteAPIView,
    RecipeApiView,
    ShoppingCartAPIView,
    SubscribeAPIView,
    TagApiView,
)


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
    
users_urlpatterns = [
    path('auth/', include('djoser.urls.authtoken')),
    path('auth/', include('djoser.urls')),
    path('subscriptions/', SubscribeAPIView.as_view()),
    path('<int:pk>/subscribe/', SubscribeAPIView.as_view())
]

urlpatterns.extend(users_urlpatterns)