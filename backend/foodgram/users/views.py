from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.pagination import LimitOffsetPagination
from users.serializers import FollowSerializer
from users.models import Follow


User = get_user_model()


class SubscribeAPIView(ListAPIView):
    pagination_class = LimitOffsetPagination
    serializer_class = FollowSerializer

    def get_queryset(self):
        return Follow.objects.filter(user=self.request.user)

    def post(self, request, pk=None):
        if pk is not None:
            author = get_object_or_404(User, id=pk)
            new_follow = request.user.new_follow(author)
            if new_follow is not None:
                serializer = FollowSerializer(new_follow)
                return Response(serializer.data, status=201)
        return Response(status=400)

    def delete(self, request, pk=None):
        if pk is not None:
            author = get_object_or_404(User, id=pk)
            result = request.user.unsubscribe_from(author)
            return Response(status=204)
        if not result:
            return Response(status=400)
