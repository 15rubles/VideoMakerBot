from django.urls import path
from . import views

urlpatterns = [
    path('youtube_api/basic_info/', views.youtube_api_basic_info),
]