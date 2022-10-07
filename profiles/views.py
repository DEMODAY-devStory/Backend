from .serializers import *

from rest_framework.viewsets import ModelViewSet


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
