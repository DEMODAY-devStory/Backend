from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import *

router = DefaultRouter()

router.register('user', UserView)

urlpatterns = router.get_urls()

urlpatterns += [
    path('login/', UserLoginView.as_view()),
    path('password_reset/', include('django_rest_passwordreset.urls'), name='password_reset'),
]
