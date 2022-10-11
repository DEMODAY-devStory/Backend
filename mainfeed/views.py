from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from account.models import User

from .serializers import *


class RecommendView(ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = RecommendSerializer

    def retrieve(self, request, *args, **kwargs):
        queryset = Profile.objects.exclude(user=self.request.user).filter(Hashtag=kwargs['pk'])
        following_list = User.objects.get(id=self.request.user).follower.values_list('following_id', flat=True)
        for following in following_list:
            queryset = queryset.exclude(user=following)
        serializer = self.get_serializer(queryset[:5], many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
