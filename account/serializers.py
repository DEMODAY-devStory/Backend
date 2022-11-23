from .models import User
from rest_framework import serializers
from django.contrib.auth import authenticate


class UserSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=255, read_only=True)
    image = serializers.ImageField(required=False)

    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'name', 'image', 'token', 'link')
        extra_kwargs = {"password": {"write_only": True}}
        read_only_fields = ('token',)

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserLoginSerializer(serializers.Serializer):
    id = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        id = data.get("id", None)
        password = data.get("password", None)
        user = authenticate(id=id, password=password)

        return user
