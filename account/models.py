from django.contrib.auth.hashers import make_password
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.utils import timezone
import uuid

class UserManager(BaseUserManager):

    def _create_user(self, email, password, **extra_fields):
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
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

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(max_length=50, unique=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    before_last_login = models.DateTimeField(default=timezone.now)
    nickname = models.CharField(max_length=15)
    name = models.CharField(max_length=15)
    image = models.ImageField(null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nickname', 'name']

    objects = UserManager()

    def __str__(self):
        return self.email

    class Meta:
        db_table = "user"
