from django.urls import path
from .views import UserView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

urlpatterns = router.get_urls()

urlpatterns += [
    path('signup/', UserView.as_view()),
    # path('login/', UserLoginView.as_view()),
]
