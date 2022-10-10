from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action

from .serializers import *
from account.models import User


class ProfileView(ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    lookup_field = "user"

    @action(detail=True, methods=['get'])
    def recommand_friends(self, request, hashtag):
        queryset = Profile.objects.exclude(user=self.request.user) #자기자신 제외
        queryset.exclude(user=User.follower).filter(Hashtag=hashtag) #자기가 팔로우하는 사람 제외
        serializer = self.get_serializer(queryset[:5:], many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class StudyView(ModelViewSet):
    queryset = Study.objects.all()
    serializer_class = StudySerializer
    lookup_field = "profile"


class HashtagView(ModelViewSet):
    queryset = Hashtag.objects.all()
    serializer_class = HashtagSerializer

    @action(detail=True, methods=['get'])
    def get_hashtag(self, request, user):
        queryset = self.queryset.filter(profile=user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'])
    def get_user(self, request, hashtag):
        queryset = self.queryset.filter(hashtag_name=hashtag)
        serializer = self.get_serializer(queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['delete'])
    def destroy(self, request, hashtag):
        queryset = self.queryset.get(hashtag_name=hashtag)
        queryset.profile.remove(Profile.objects.get(user=request.user))
        if not queryset.profile:
            self.perform_destroy(queryset)
        return Response(status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        try:
            queryset = self.queryset.get(hashtag_name=request.data['hashtag_name'])
            queryset.profile.add(Profile.objects.get(user=request.user))
            return Response(status=status.HTTP_201_CREATED)
        except Exception:
            return super().create(request, *args, **kwargs)


class SkillView(ModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer


class ProjectView(ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class CareerView(ModelViewSet):
    queryset = Career.objects.all()
    serializer_class = CareerSerializer


class FollowView(ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    lookup_field = "user"

    # url: follow/{id}/{function_name}
    @action(detail=True, methods=['get'])
    def get_following(self, request, user):
        queryset = self.queryset.filter(follower=user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'])
    def get_follower(self, request, user):
        queryset = self.queryset.filter(following=user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:  # unfollow
            instance = self.queryset.get(
                following=serializer.data['following']
                , follower=serializer.data['follower'])
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception:  # follow
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(status=status.HTTP_201_CREATED, headers=headers)
