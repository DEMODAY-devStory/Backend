from django.contrib.auth import login, logout
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
            # 데이터가 unique하지 않음
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            # 기타 오류 (발생하면 안 됨)
            return Response(exception=Exception)

        serializer.save()
        return Response(status=status.HTTP_201_CREATED)


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
            login(request, user)
            user = UserSerializer(user)
            return Response(data={'id': user.data['id'], 'img': user.data['image']}
                            , status=status.HTTP_200_OK)


@method_decorator(csrf_exempt, name='dispatch')
@api_view(('GET',))
def userLogoutView(request):
    logout(request)
    return Response(status=status.HTTP_200_OK)
