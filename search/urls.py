from django.urls import path
from .views import *

urlpatterns = [
    path('<str:string>/', SearchView.as_view()),
]
