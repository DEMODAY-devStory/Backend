from rest_framework import status
from rest_framework.response import Response

from .serializers import *

from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action


class ProfileView(ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    lookup_field = "user"


class StudyView(ModelViewSet):
    queryset = Study.objects.all()
    serializer_class = StudySerializer
    lookup_field = "profile"


class HashtagView(ModelViewSet):
    queryset = Hashtag.objects.all()
    serializer_class = HashtagSerializer
    lookup_field = "profile"


class SkillView(ModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    lookup_field = "profile"


class ProjectView(ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProfileSerializer
    lookup_field = "profile"


class CareerView(ModelViewSet):
    queryset = Career.objects.all()
    serializer_class = CareerSerializer
    lookup_field = "profile"


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
