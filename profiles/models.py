from secrets import choice
from unittest.util import _MAX_LENGTH
from django.db import models
from django.conf import settings
from requests import delete


class profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    image = models.ImageField()
    followerNum = models.IntegerField()
    followingNum = models.IntegerField()
    hashtag = models.CharField(max_length=255, null=True)
    belong = models.CharField(max_length=255, null=True)
    mainposition = models.CharField(max_length=255, null=True)
    subposition = models.CharField(max_length=255, null=True)
    readme = models.TextField(null=True, blank=True)


class skill(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    skill_name = models.CharField(max_length=255, null=True)
    CHOICE = (
        ('pl', 'programming language'),
        ('fl', 'framework or library')
    )
    skill_type = models.CharField(max_lengh=20, choice=CHOICE)


class project(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=255, null=True)
    position = models.CharField(max_length=255, null=True)
    skill = models.ForeignKey(skill,)
    start_year = models.CharField(max_length=255, null=True)
    start_month = models.CharField(max_length=255, null=True)
    end_year = models.CharField(max_length=255, null=True)
    end_month = models.CharField(max_length=255, null=True)
    detail = models.TextField(null=True, blank=True)
