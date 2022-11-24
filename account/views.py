import uuid
import boto3 as boto3

from django.utils import timezone
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from devs import settings
from .serializers import *

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


@method_decorator(csrf_exempt, name='dispatch')
class UserView(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = (AllowAny,)
    lookup_field = "id"

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response(exception=Exception)

        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        data = request.data.copy()
        # image to aws s3
        if request.data['image']:
            image_url = S3ImgUploader(request.data['image']).upload()
            data['image'] = "https://devstory-bucket.s3.amazonaws.com/" + image_url
        print(data['image'])

        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


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
            user.last_login = timezone.now()
            user.save()
            user_data = UserSerializer(user).data
            return Response(
                data={
                    'id': user_data['id'], 'img': user_data['image']
                    , 'token': user.token.decode('utf-8')
                }
                , status=status.HTTP_200_OK)


class S3ImgUploader:
    def __init__(self, file):
        self.file = file

    def upload(self):
        s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
        )
        url = 'img' + '/' + uuid.uuid1().hex

        s3_client.upload_fileobj(
            self.file,
            settings.S3_BUCKET_NAME,
            url,
            ExtraArgs={
                "ContentType": self.file.content_type
            }
        )
        return url
