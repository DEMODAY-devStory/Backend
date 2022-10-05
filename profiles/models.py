from django.db import models
from django.conf import settings

MAX_LENGTH = 100


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    belong = models.CharField(max_length=MAX_LENGTH, null=True)
    main_position = models.CharField(max_length=MAX_LENGTH, null=True)
    sub_position = models.CharField(max_length=MAX_LENGTH, null=True)
    introduction = models.TextField(null=True, blank=True)


class Skill(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    skill_name = models.CharField(max_length=MAX_LENGTH, null=True)
    CHOICE = (
        ('pl', 'programming language'),
        ('fl', 'framework or library')
    )
    skill_type = models.CharField(max_length=20, choices=CHOICE)


class Project(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    project_name = models.CharField(max_length=MAX_LENGTH, null=True)
    position = models.CharField(max_length=MAX_LENGTH, null=True)
    skill = models.CharField(max_length=MAX_LENGTH, null=True)
    coworker = models.CharField(max_length=MAX_LENGTH, null=True)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    detail = models.TextField(null=True, blank=True)


class Career(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    company = models.CharField(max_length=MAX_LENGTH, null=True)
    position = models.CharField(max_length=MAX_LENGTH, null=True)
    locate = models.CharField(max_length=MAX_LENGTH, null=True)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    skill = models.CharField(max_length=MAX_LENGTH, null=True)
    detail = models.TextField(null=True, blank=True)
