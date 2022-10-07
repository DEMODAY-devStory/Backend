from django.urls import path
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('profile', ProfileView)
router.register('study', StudyView)
router.register('hashtag', HashtagView)
router.register('skill', SkillView)
router.register('project', ProjectView)
router.register('career', CareerView)
router.register('follow', FollowView)

urlpatterns = router.get_urls()