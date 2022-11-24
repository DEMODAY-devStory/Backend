from datetime import datetime, timedelta

import jwt
from django.contrib.auth.hashers import make_password
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.utils import timezone

from devs import settings
from profiles.models import Profile, Study

from django.dispatch import receiver
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail


class UserManager(BaseUserManager):

    def _create_user(self, email, password, **extra_fields):
        user = self.model(email=email, **extra_fields)
        user.last_login = timezone.now()
        user.password = make_password(password)
        user.save(using=self._db)

        # 회원가입 시 프로필, 현재공부중 자동 생성
        profile = Profile(user=user)
        profile.save()
        Study(profile=profile).save()
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    id = models.CharField(max_length=20, unique=True, primary_key=True)
    email = models.EmailField(max_length=50, unique=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    before_last_login = models.DateTimeField(default=timezone.now)
    name = models.CharField(max_length=15)
    image = models.TextField(null=True, blank=True,
                             default="https://" + settings.S3_BUCKET_NAME + ".s3.amazonaws.com/img/profile-img.png")
    updated_at = models.DateTimeField(auto_now=True)
    link = models.URLField(max_length=100, null=True, blank=True)

    USERNAME_FIELD = 'id'
    REQUIRED_FIELDS = ['email', 'name']

    objects = UserManager()

    def __str__(self):
        return self.id

    @property
    def token(self):
        return self._generate_jwt_token()

    def _generate_jwt_token(self):
        dt = datetime.now() + timedelta(days=60)

        token = jwt.encode({
            'id': self.pk,
            'exp': dt.utcfromtimestamp(dt.timestamp())
        }, settings.SECRET_KEY, algorithm='HS256')

        return token

    class Meta:
        db_table = "user"


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    email_plaintext_message = "토큰과 새 비밀번호를 입력해주세요! \ntoken = {}".format(reset_password_token.key)

    send_mail(
        # title:
        "devStory에서 비밀번호를 변경합니다",
        # message:
        email_plaintext_message,
        # from:
        "taeho205@likelion.org",
        # to:
        [reset_password_token.user.email]
    )
