from django.shortcuts import render

from django.views.generic import (
    View,
)

from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener

from . import twitter_credentials

class StdOutListener(StreamListener):

    def on_data(self, data):
        print(data)
        return True

    def on_error(self, status):
        print(status)

class StreamerView(View):
    template_name = 'tweepy_streamer/streamer.html'

    def get(self, request, *args, **kwargs):
        
        listener = StdOutListener()
        
        auth = OAuthHandler(twitter_credentials.CONSUMER_KEY, twitter_credentials.CONSUMER_SECRET)
        auth.set_access_token(twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKON_SECRET)

        stream = Stream(auth, listener)

        stream.filter(track=['lebron james', 'kevin durant', 'stephen curry', 'james harden'])

        return render(request, self.template_name, {})

