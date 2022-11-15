from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action

from .serializers import *

from account.models import User


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

    @action(detail=True, methods=['get'])
    def get_fl(self, request, user):
        queryset = self.queryset.filter(profile=user, skill_type='fl')
        serializer = self.get_serializer(queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'])
    def get_pl(self, request, user):
        queryset = self.queryset.filter(profile=user, skill_type='pl')
        serializer = self.get_serializer(queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class SkillDetailView(ModelViewSet):
    queryset = SkillDetail.objects.all()
    serializer_class = SkillDetailSerializer

    def retrieve(self, request, *args, **kwargs):
        queryset = self.queryset.filter(skill_name=kwargs['pk'])
        serializer = self.get_serializer(queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class SkillDetailContentView(ModelViewSet):
    queryset = SkillDetail.objects.all()
    serializer_class = SkillDetailSerializer

    def retrieve(self, request, *args, **kwargs):
        queryset = self.queryset.filter(skill_name=kwargs['skilldetail_pk']).filter(id=kwargs['skill_pk'])
        serializer = self.get_serializer(queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        queryset = self.queryset.get(skill_name=kwargs['skilldetail_pk'], id=kwargs['skill_pk'])
        serializer = self.get_serializer(queryset, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.queryset.get(skill_name=kwargs['skilldetail_pk'], id=kwargs['skill_pk'])
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProjectView(ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def retrieve(self, request, *args, **kwargs):
        queryset = self.queryset.filter(profile=kwargs['pk'])
        serializer = self.get_serializer(queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class CareerView(ModelViewSet):
    queryset = Career.objects.all()
    serializer_class = CareerSerializer

    def retrieve(self, request, *args, **kwargs):
        queryset = self.queryset.filter(profile=kwargs['pk'])
        serializer = self.get_serializer(queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class FollowView(ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    lookup_field = "user"

    # url: follow/{id}/{function_name}
    @action(detail=True, methods=['get'])
    def get_following(self, request, user):
        following_list = self.queryset.filter(follower=user).values_list('following', flat=True)
        queryset = list()
        for following in following_list:
            instance = dict()
            instance['user'] = following
            instance['image'] = User.objects.get(id=following).image
            instance['position'] = Profile.objects.get(user_id=following).main_position
            queryset.append(instance)
        serializer = GetFollowSerializer(queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'])
    def get_follower(self, request, user):
        follower_list = self.queryset.filter(following=user).values_list('follower', flat=True)
        queryset = list()
        for follower in follower_list:
            instance = dict()
            instance['user'] = follower
            instance['image'] = User.objects.get(id=follower).image
            instance['position'] = Profile.objects.get(user_id=follower).main_position
            queryset.append(instance)
        serializer = GetFollowSerializer(queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:  # unfollow
            instance = self.queryset.get(
                following=serializer.initial_data['following']
                , follower=serializer.initial_data['follower'])
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception:  # follow
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(status=status.HTTP_201_CREATED, headers=headers)


class IsFollowView(RetrieveAPIView):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = dict()
        try:
            get_object_or_404(Follow, follower=request.user, following=kwargs['pk'])
            instance['is_follow'] = True
        except:
            instance['is_follow'] = False

        serializer = IsFollowSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
