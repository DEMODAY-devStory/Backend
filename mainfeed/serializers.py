from rest_framework import serializers
from account.models import User
from profiles.models import Follow
from profiles.models import Profile

class FriendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile, Follow
        fields = '__all__'
