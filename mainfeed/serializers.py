from rest_framework import serializers
from account.models import User
from profiles.models import Follow
from profiles.models import Profile

class FriendsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'
