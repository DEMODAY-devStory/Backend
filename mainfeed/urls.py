from django.urls import path
from .views import *

urlpatterns = [
    path('recommand/<str:hashtag>/', RecommendView.as_view({'get': 'retrieve'})),
]
