from gc import get_objects
from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.permissions import AllowAny

from .serializers import UserSerializer
from .models import User

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


@method_decorator(csrf_exempt, name='dispatch')
class UserView(CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except:
            status_code = status.HTTP_200_OK
            return Response({'success': "false", 'status code': status_code, }, status=status_code)
        serializer.save()  # serializer 내부의 create() 호출
        status_code = status.HTTP_201_CREATED  # 성공
        response = {
            'success': "true",
            'status code': status_code,
        }
        return Response(response, status=status_code)


# @method_decorator(csrf_exempt, name='dispatch')
# class UserLoginView(GenericAPIView):
#     permission_classes = (AllowAny,)
#     serializer_class = UserLoginSerializer

#     def post(self, request):
#         serializer = self.serializer_class(data=request.data)
#         user = serializer.validate(request.data)

#         if user is None:
#             response = {
#                 "success": "false",
#                 "status_code": status.HTTP_200_OK,
#                 "id": "",
#             }
#         else:
#             try:
#                 img = UserImg.objects.get(user_id=user.id).image
#             except:
#                 img = ""
#             response = {
#                 "success": "true",
#                 "status_code": status.HTTP_200_OK,
#                 "id": user.id,
#                 "img": str(img),
#             }

#         return Response(response, status=status.HTTP_200_OK)
