from django.urls import path

from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('profile', ProfileView)
router.register('study', StudyView)
router.register('project', ProjectView)
router.register('career', CareerView)
router.register('follow', FollowView)
router.register('skill', SkillView)
router.register('skilldetail', SkillDetailView)

urlpatterns = router.get_urls()
urlpatterns += [
    path('hashtag/', HashtagView.as_view({'post': 'create'})),
    path('hashtag/<str:hashtag>/', HashtagView.as_view({'delete': 'destroy'})),
    path('hashtag/get_user/<str:hashtag>/', HashtagView.as_view({'get': 'get_user'})),
    path('hashtag/get_hashtag/<str:user>/', HashtagView.as_view({'get': 'get_hashtag'})),
    path('skill/get_fl/<str:user>/', SkillView.as_view({'get': 'get_fl'})),
    path('skill/get_pl/<str:user>/', SkillView.as_view({'get': 'get_pl'})),
    # path('skill/', SkillView.as_view({'post': 'create'})),
    # path('skill/<int:pk>/', SkillView.as_view({'delete': 'destroy', 'get': 'retrieve'})),
    path('skilldetail/<int:skilldetail_pk>/<int:skill_pk>/', SkillDetailContentView.as_view({'get': 'retrieve', 'patch': 'update', 'delete': 'destroy'})),
    path('isfollow/<str:follower>/<str:following>/', IsFollowView.as_view()),
]
