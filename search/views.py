from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status

from profiles.models import *
from account.models import *


class SearchView(ListAPIView):
    def get_queryset(self):
        return None

    def list(self, request, *args, **kwargs):
        search_string = kwargs['string']
        searched_profiles = set()

        hashtags = Hashtag.objects.filter(hashtag_name__icontains=search_string)
        for hashtag in hashtags:
            profiles_queryset = hashtag.profile.all().values_list('user_id', flat=True)
            searched_profiles.update(profiles_queryset)

        users = User.objects.exclude(id=self.request.user.id) \
            .filter(id__icontains=search_string).values_list('id', flat=True)
        searched_profiles.update(users)

        names = User.objects.exclude(id=self.request.user.id)\
            .filter(name__icontains=search_string).values_list('id', flat=True)
        searched_profiles.update(names)

        return Response(data={"ids": searched_profiles}, status=status.HTTP_200_OK)
