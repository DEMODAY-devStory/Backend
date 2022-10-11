from rest_framework import status, generics
import operator
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import ListAPIView

from account.models import User
from profiles.models import Hashtag

from .serializers import *
from profiles.serializers import *


class RecommendView(ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = RecommendSerializer

    def list(self, request, *args, **kwargs):
        my_profile = Profile.objects.get(user=self.request.user)
        my_hashtag = Hashtag.objects.filter(profile=my_profile).values_list('hashtag_name', flat=True)

        user_queryset = Profile.objects.exclude(user=self.request.user).filter(Hashtag=kwargs['pk']).values_list('user',
                                                                                                                 flat=True)
        following_queryset = User.objects.get(id=self.request.user).follower.values_list('following_id', flat=True)
        user_list = list(set(user_queryset) - set(following_queryset))

        commonhash_dict = {}
        for user in user_list:
            following_hashtag = Hashtag.objects.filter(profile=user).values_list('hashtag_name', flat=True)
            common = len(set(following_hashtag) & set(my_hashtag))
            commonhash_dict[user] = common

        commonhash_dict = dict(sorted(commonhash_dict.items(), key=operator.itemgetter(1), reverse=True))

        queryset = []
        for user in commonhash_dict:
            queryset.append(Profile.objects.get(user=user))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset[:5], many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class FeedView(generics.ListAPIView):

    def get_queryset(self):
        return None

    def list(self, request, *args, **kwargs):
        last_login = self.request.user.before_last_login
        idols = Follow.objects.filter(follower=self.request.user)
        instances = []
        for idol in idols:
            profile = Profile.objects.get(user=idol.following)
            if profile.updated_at > last_login:
                instances.append(ProfileSerializer(profile).data)

            study = Study.objects.get(profile=profile)
            if study.updated_at > last_login:
                instances.append(StudySerializer(study).data)

            skills = Skill.objects.filter(profile=profile)
            for skill in skills:
                skillDetails = SkillDetail.objects.filter(skill_name=skill)
                for skillDetail in skillDetails:
                    if skillDetail.updated_at > last_login:
                        instances.append(SkillDetailSerializer(skillDetail).data)

            projects = Project.objects.filter(profile=profile)
            for project in projects:
                if project.updated_at > last_login:
                    instances.append(ProjectSerializer(project).data)

            careers = Career.objects.filter(profile=profile)
            for career in careers:
                if career.updated_at > last_login:
                    instances.append(CareerSerializer(career).data)

        return Response(data=instances, status=status.HTTP_200_OK)
