from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from account.models import User
from profiles.serializers import *


class RecommendView(ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def retrieve(self, request, *args, **kwargs):
        # 접속한 유저의 팔로잉이 아니면서 해당 해시태그를 가진 유저들
        queryset = Profile.objects.exclude(user=self.request.user).filter(Hashtag=kwargs['pk'])
        following_list = User.objects.get(id=self.request.user).follower.values_list('following_id', flat=True)
        for following in following_list:
            queryset = queryset.exclude(user=following)
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
