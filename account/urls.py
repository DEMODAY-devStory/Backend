from django.urls import path
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('user', UserView)

urlpatterns = router.get_urls()

urlpatterns += [
    path('signup/', UserSignUpView.as_view()),
    path('login/', UserLoginView.as_view()),
    path('logout/', userLogoutView),
]
