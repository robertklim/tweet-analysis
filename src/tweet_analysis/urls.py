from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('streamer/', include('tweepy_streamer.urls', namespace='tweepy-streamer')),
]
