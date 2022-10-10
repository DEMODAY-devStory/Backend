from rest_framework import serializers
from profiles.models import Profile

class RecommandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'
