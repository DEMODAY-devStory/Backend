from dataclasses import fields
from .models import User
from rest_framework import serializers
from django.contrib.auth import authenticate


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'name', 'image')
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    # TODO: 회원정보 수정 시 update 함수 override


class UserLoginSerializer(serializers.Serializer):
    id = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        id = data.get("id", None)
        password = data.get("password", None)
        user = authenticate(id=id, password=password)

        return user
