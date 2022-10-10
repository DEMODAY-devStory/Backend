from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action

from account.models import User

from .serializers import *

class FriendsView(ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = FriendsSerializer

    @action(detail=True, methods=['get'])
    def recommand_friends(self, request, hashtag):
        queryset = Profile.objects.exclude(user=self.request.user).filter(Hashtag=hashtag) # 자기자신 제외 해시태그 갖고있는 사람들
        following_list = User.objects.get(id=self.request.user).follower.values_list('following_id', flat=True) # request user가 팔로우하고 있는 사람 리스트
        for i in following_list: queryset = queryset.exclude(user=i) # 리스트에서 한 명 씩 제거
        serializer = self.get_serializer(queryset[:5], many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
        # return Response(data=[0], status=status.HTTP_200_OK)
