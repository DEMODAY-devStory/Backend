from django.contrib.auth import login, logout, authenticate
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from .serializers import *

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


@method_decorator(csrf_exempt, name='dispatch')
class UserView(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)
    lookup_field = "id"

    def create(self, request, *args, **kwargs):  # 회원가입
        serializer = self.serializer_class(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response(exception=Exception)

        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)


@method_decorator(csrf_exempt, name='dispatch')
class UserLoginView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        user = serializer.validate(request.data)

        if user is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            user.before_last_login = user.last_login
            user.save()
            user_data = UserSerializer(user).data
            return Response(
                data={
                    'id': user_data['id'], 'img': user_data['image']
                    , 'token': user.token.decode('utf-8')
                }
                , status=status.HTTP_200_OK)
