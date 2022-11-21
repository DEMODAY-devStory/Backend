import operator
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import ListAPIView

from account.models import User
from profiles.serializers import *


class RecommendView(ListAPIView):
    serializer_class = ProfileSerializer

    def get_queryset(self):
        return None

    def list(self, request, *args, **kwargs):
        my_profile = Profile.objects.get(user=self.request.user)
        my_hashtag = Hashtag.objects.filter(profile=my_profile).values_list('hashtag_name', flat=True)

        user_queryset = Profile.objects.exclude(user=self.request.user).filter(Hashtag=kwargs['pk']).values_list('user',
                                                                                                                 flat=True)
        following_queryset = User.objects.get(id=self.request.user).follower.values_list('following_id', flat=True)
        user_list = list(set(user_queryset) - set(following_queryset))

        common_hash = dict()
        for user in user_list:
            following_hashtag = Hashtag.objects.filter(profile=user).values_list('hashtag_name', flat=True)
            common = len(set(following_hashtag) & set(my_hashtag))
            common_hash[user] = common

        common_hash = dict(sorted(common_hash.items(), key=operator.itemgetter(1), reverse=True))

        queryset = list()
        for user in common_hash:
            queryset.append(Profile.objects.get(user=user))

        serializer = self.get_serializer(queryset[:5], many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class FeedView(ListAPIView):
    def get_queryset(self):
        return None

    def list(self, request, *args, **kwargs):

        updated_idols = set()
        last_login = self.request.user.before_last_login
        idols = Follow.objects.filter(follower=self.request.user)
        instances = list()
        for idol in idols:
            profile = Profile.objects.get(user=idol.following)
            if profile.updated_at > last_login:
                updated_idols.add(idol.following.id)
                serializer = dict()
                serializer['user'] = str(idol.following.id)
                serializer['update'] = "프로필"
                serializer['updated_at'] = profile.updated_at
                instances.append(serializer)

            study = Study.objects.get(profile=profile)
            if study.updated_at > last_login:
                updated_idols.add(idol.following.id)
                serializer = dict()
                serializer['user'] = str(idol.following.id)
                serializer['update'] = "현재 진행 중"
                serializer['updated_at'] = study.updated_at
                instances.append(serializer)

            skills = Skill.objects.filter(profile=profile)
            for skill in skills:
                skillDetails = SkillDetail.objects.filter(skill_name=skill)
                for skillDetail in skillDetails:
                    if skillDetail.updated_at > last_login:
                        updated_idols.add(idol.following.id)
                        serializer = dict()
                        serializer['user'] = str(idol.following.id)
                        if skill.skill_type == 'pl':
                            serializer['update'] = "기술스택/Programming Language/{}".format(skill.skill_name)
                        else:
                            serializer['update'] = "기술스택/Framework & Library/{}".format(skill.skill_name)
                        serializer['updated_at'] = skillDetail.updated_at
                        instances.append(serializer)

            projects = Project.objects.filter(profile=profile)
            for project in projects:
                if project.updated_at > last_login:
                    updated_idols.add(idol.following.id)
                    serializer = dict()
                    serializer['user'] = str(idol.following.id)
                    serializer['update'] = "프로젝트/{}".format(project.project_name)
                    serializer['updated_at'] = project.updated_at
                    instances.append(serializer)

            careers = Career.objects.filter(profile=profile)
            for career in careers:
                if career.updated_at > last_login:
                    updated_idols.add(idol.following.id)
                    serializer = dict()
                    serializer['user'] = str(idol.following.id)
                    serializer['update'] = "경력/{}".format(career.company)
                    serializer['updated_at'] = career.updated_at
                    instances.append(serializer)

        instances.sort(key=lambda instance: instance['updated_at'], reverse=True)
        return Response(data={"feed": instances, "updated_id": updated_idols}, status=status.HTTP_200_OK)
