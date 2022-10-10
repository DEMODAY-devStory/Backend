from django.urls import path
from .views import *

urlpatterns = [
    path('recommand/<str:hashtag>/', RecommandView.as_view({'get': 'retrieve'})),
]
