from django.shortcuts import render

from django.views.generic import (
    View,
)

class StreamerView(View):
    template_name = 'tweepy_streamer/streamer.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})

