# podcast_resources/urls.py
from django.urls import path
from .views import PodcastTestView  # example

urlpatterns = [
    path('test/', PodcastTestView.as_view(), name='podcast-test'),
]
