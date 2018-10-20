from django.urls import path

from .views import StreamerView

app_name = 'tweepy-streamer'

urlpatterns = [
    path('', StreamerView.as_view(), name='streamer'),
]