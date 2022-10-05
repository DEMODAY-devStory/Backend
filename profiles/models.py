from django.db import models
from django.conf import settings

MAX_LENGTH = 100


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    belong = models.CharField(max_length=MAX_LENGTH, null=True)
    main_position = models.CharField(max_length=MAX_LENGTH, null=True)
    sub_position = models.CharField(max_length=MAX_LENGTH, null=True)
    introduction = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user)


class Study(models.Model):
    profile = models.OneToOneField('Profile', on_delete=models.CASCADE)
    current_study = models.CharField(max_length=MAX_LENGTH, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.current_study) + " " + str(self.profile)


class Hashtag(models.Model):
    hashtag_name = models.CharField(max_length=20, primary_key=True)
    profile = models.ManyToManyField('Profile')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.hashtag_name)


class Skill(models.Model):
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE)
    skill_name = models.CharField(max_length=MAX_LENGTH, null=True)
    CHOICE = (
        ('pl', 'programming language'),
        ('fl', 'framework or library')
    )
    skill_type = models.CharField(max_length=20, choices=CHOICE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.skill_name) + " " + str(self.profile)


class Project(models.Model):
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE)
    project_name = models.CharField(max_length=MAX_LENGTH, null=True)
    position = models.CharField(max_length=MAX_LENGTH, null=True)
    skill = models.CharField(max_length=MAX_LENGTH, null=True)
    coworker = models.CharField(max_length=MAX_LENGTH, null=True)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    detail = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.project_name) + " " + str(self.profile)


class Career(models.Model):
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE)
    company = models.CharField(max_length=MAX_LENGTH, null=True)
    position = models.CharField(max_length=MAX_LENGTH, null=True)
    locate = models.CharField(max_length=MAX_LENGTH, null=True)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    skill = models.CharField(max_length=MAX_LENGTH, null=True)
    detail = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.company) + " " + str(self.profile)


class Follow(models.Model):
    follower = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='follower')
    following = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='following')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.follower) + " follows " + str(self.following)
