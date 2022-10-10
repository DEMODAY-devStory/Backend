from django.urls import path

from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('profile', ProfileView)
router.register('study', StudyView)
router.register('skill', SkillView)
router.register('project', ProjectView)
router.register('career', CareerView)
router.register('follow', FollowView)

urlpatterns = router.get_urls()
urlpatterns += [
    path('hashtag/', HashtagView.as_view({'post': 'create'})),
    path('hashtag/<str:hashtag>/', HashtagView.as_view({'delete': 'destroy'})),
    path('hashtag/get_user/<str:hashtag>/', HashtagView.as_view({'get': 'get_user'})),
    path('hashtag/get_hashtag/<str:user>/', HashtagView.as_view({'get': 'get_hashtag'})),
]
