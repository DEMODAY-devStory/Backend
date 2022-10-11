from django.urls import path
from .views import *

urlpatterns = [
    path('recommend/<str:pk>/', RecommendView.as_view({'get': 'retrieve'})),
    path('', FeedView.as_view()),
]
