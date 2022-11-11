from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import *

router = DefaultRouter()

router.register('user', UserView)

urlpatterns = router.get_urls()

urlpatterns += [
    path('login/', UserLoginView.as_view()),
]
