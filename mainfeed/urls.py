from django.urls import path
# from rest_framework.routers import DefaultRouter
from .views import *

# router = DefaultRouter()
# urlpatterns = router.get_urls()

urlpatterns = [
    path('recommand-friends/<str:hashtag>/', FriendsView.as_view({'get': 'recommand_friends'})),
]
