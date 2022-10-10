from django.db import models
from django.conf import settings

MAX_LENGTH = 100


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
        , related_name='Profile', primary_key=True)
    belong = models.CharField(max_length=MAX_LENGTH, null=True, blank=True)
    main_position = models.CharField(max_length=MAX_LENGTH, null=True, blank=True)
    sub_position = models.CharField(max_length=MAX_LENGTH, null=True, blank=True)
    introduction = models.TextField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    def __str__(self):
        return str(self.user)


class Study(models.Model):
    profile = models.OneToOneField(
        'Profile', on_delete=models.CASCADE, related_name='Study', primary_key=True)
    current_study = models.CharField(max_length=MAX_LENGTH, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    def __str__(self):
        return str(self.current_study) + " " + str(self.profile)


class Hashtag(models.Model):
    hashtag_name = models.CharField(max_length=20, primary_key=True)
    profile = models.ManyToManyField('Profile', related_name='Hashtag')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    def __str__(self):
        return str(self.hashtag_name)


class Skill(models.Model):
    profile = models.ForeignKey(
        'Profile', on_delete=models.CASCADE, related_name='Skill')
    skill_name = models.CharField(max_length=MAX_LENGTH)
    CHOICE = (
        ('pl', 'programming language'),
        ('fl', 'framework or library')
    )
    skill_type = models.CharField(max_length=20, choices=CHOICE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    def __str__(self):
        return str(self.skill_name) + " " + str(self.profile)


class SkillDetail(models.Model):
    skill_name = models.ForeignKey(
        'Skill', on_delete=models.CASCADE, related_name='SkillDetail'
    )
    skill_detail = models.CharField(max_length=MAX_LENGTH)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    def __str__(self):
        return str(self.skill_name) + " " + str(self.skill_detail)


class Project(models.Model):
    profile = models.ForeignKey(
        'Profile', on_delete=models.CASCADE, related_name='Project')
    project_name = models.CharField(max_length=MAX_LENGTH)
    position = models.CharField(max_length=MAX_LENGTH, null=True, blank=True)
    skill = models.CharField(max_length=MAX_LENGTH, null=True, blank=True)
    coworker = models.CharField(max_length=MAX_LENGTH, null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    detail = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    def __str__(self):
        return str(self.project_name) + " " + str(self.profile)


class Career(models.Model):
    profile = models.ForeignKey(
        'Profile', on_delete=models.CASCADE, related_name='Career')
    company = models.CharField(max_length=MAX_LENGTH)
    position = models.CharField(max_length=MAX_LENGTH, null=True, blank=True)
    locate = models.CharField(max_length=MAX_LENGTH, null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    skill = models.CharField(max_length=MAX_LENGTH, null=True, blank=True)
    detail = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    def __str__(self):
        return str(self.company) + " " + str(self.profile)


class Follow(models.Model):
    follower = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='follower')
    following = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='following')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    def __str__(self):
        return str(self.follower) + " follows " + str(self.following)
