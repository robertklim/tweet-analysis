from django.shortcuts import render

from django.views.generic import (
    View,
)

from tweepy import API
from tweepy import Cursor
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener

from . import twitter_credentials
import numpy as np
import pandas as pd

class TwitterClient():
    def __init__(self, twitter_user=None):
        self.auth = TwitterAuthenticator().authenticate_twitter_app()
        self.twitter_client = API(self.auth)
        self.twitter_user = twitter_user

    def get_twitter_client_api(self):
        return self.twitter_client

    def get_user_timeline_tweets(self, num_tweets):
        tweets = []
        for tweet in Cursor(self.twitter_client.user_timeline, id=self.twitter_user).items(num_tweets):
            tweets.append(tweet)
        return tweets

    def get_friend_list(self, num_friends):
        friend_list=[]
        for friend in Cursor(self.twitter_client.friends, id=self.twitter_user).items(num_friends):
            friend_list.append(friend)
        return friend_list

    def get_home_timeline_tweets(self, num_tweets):
        home_timeline_tweets = []
        for tweet in Cursor(self.twitter_client.home_timeline, id=self.twitter_user).items(num_tweets):
            home_timeline_tweets.append(tweet)
        return home_timeline_tweets

class TwitterAuthenticator():

    def authenticate_twitter_app(self):
        auth = OAuthHandler(twitter_credentials.CONSUMER_KEY, twitter_credentials.CONSUMER_SECRET)
        auth.set_access_token(twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKON_SECRET)
        return auth

class TwitterStreamer():

    def __init__(self):
        self.twitter_authenticator = TwitterAuthenticator()

    def stream_tweets(self, fetched_tweets_filename, hash_tag_list):
        listener = TwitterListener(fetched_tweets_filename)
        auth = self.twitter_authenticator.authenticate_twitter_app()
        stream = Stream(auth, listener)

        stream.filter(track=hash_tag_list)

class TwitterListener(StreamListener):

    def __init__(self, fetched_tweets_filename):
        self.fetched_tweets_filename = fetched_tweets_filename

    def on_data(self, data):
        try:
            print('writing data...')
            with open(self.fetched_tweets_filename, 'a') as tf:
                tf.write(data)
            return True
        except BaseException as e:
            print(f'Data error:{e}')
        return True

    def on_error(self, status):
        if status == '420':
            return False
        print(status)

class TweetAnalyzer():
    
    def tweets_to_data_frame(self, tweets):
        df = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['tweets'])
        
        df['id'] = np.array([tweet.id for tweet in tweets])
        df['len'] = np.array([len(tweet.text) for tweet in tweets])
        df['date'] = np.array([tweet.created_at for tweet in tweets])
        df['source'] = np.array([tweet.source for tweet in tweets])
        df['likes'] = np.array([tweet.favorite_count for tweet in tweets])
        df['retweets'] = np.array([tweet.retweet_count for tweet in tweets])

        return df

class StreamerView(View):
    template_name = 'tweepy_streamer/streamer.html'

    def get(self, request, *args, **kwargs):

        twitter_client = TwitterClient()
        tweet_analyzer = TweetAnalyzer()

        api = twitter_client.get_twitter_client_api()

        tweets = api.user_timeline(screen_name='joerogan', count=20)

        # print(dir(tweets[0]))
        # print(tweets[0].id)
        # print(tweets[0].retweet_count)

        df = tweet_analyzer.tweets_to_data_frame(tweets)
        print(df.head(10))

        # hash_tag_list = ['lebrone james', 'kevin durant', 'james harden', 'stephen curry']
        # fetched_tweets_filename = 'tweets.json'

        # twitter_client = TwitterClient()
        # print('-------------- USER TIMELINE')
        # print(twitter_client.get_user_timeline_tweets(1))
        # print('-------------- USER FRIEND LIST')
        # print(twitter_client.get_friend_list(1))
        # print('-------------- USER HOME TIMELINE')
        # print(twitter_client.get_home_timeline_tweets(1))

        # twitter_streamer = TwitterStreamer()
        # twitter_streamer.stream_tweets(fetched_tweets_filename, hash_tag_list)

        return render(request, self.template_name, {})

