import email
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action

from account.models import User

from .serializers import *

class FriendsView(ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = FriendSerializer

    @action(detail=True, methods=['get'])
    def recommand_friends(self, request, hashtag):
        users = User.objects.get(id=self.request.user)
        print(users.follower.values_list('following_id', flat=True))
        # queryset = Profile.objects.exclude(user=self.request.user).filter(Hashtag=hashtag) #자기자신 제외
        # queryset.exclude(user=self.request.user.follower).filter(Hashtag=hashtag) #자기가 팔로우하는 사람 제외
        serializer = self.get_serializer(user, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
