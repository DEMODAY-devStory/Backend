from django.urls import path
from .views import *

urlpatterns = [
    path('recommend/<str:pk>/', RecommendView.as_view()),
]
