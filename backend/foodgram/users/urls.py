from django.urls import include, path
from users.views import SubscribeAPIView

urlpatterns = [
    path('auth/', include('djoser.urls.authtoken')),
    path('auth/', include('djoser.urls')),
    path('subscriptions/', SubscribeAPIView.as_view()),
    path('<int:pk>/subscribe/', SubscribeAPIView.as_view())
]