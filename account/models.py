from email.policy import default
from django.contrib.auth.hashers import make_password
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.utils import timezone

from profiles.models import Profile, Study


class UserManager(BaseUserManager):

    def _create_user(self, email, password, **extra_fields):
        user = self.model(email=email, **extra_fields)
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
    image = models.ImageField(upload_to='users', null=True, blank=True, default='profile-img.png')
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'id'
    REQUIRED_FIELDS = ['email', 'name']

    objects = UserManager()

    def __str__(self):
        return self.id

    class Meta:
        db_table = "user"
