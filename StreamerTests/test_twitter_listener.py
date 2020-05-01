import asyncio
import datetime
import threading
import time

from twitter_listener import TwitterListener
from StreamerTests.twitter_keys_hidden import api_key, api_secret, access_token_secret, access_token
import tweepy


def push_tweet(author: str, text: str, created_at: datetime):
    print("{author} tweeted at {at}: {text}".format(author=author, at=created_at, text=text))


def on_error(msg: str):
    print("Error: " + msg)


def on_warning(msg: str):
    print("Warning: " + msg)


async def listen(source, track):
    source.filter(track=track)


auth = tweepy.OAuthHandler(api_key, api_secret)
auth.set_access_token(access_token, access_token_secret)

listener = TwitterListener(push_tweet, on_error, on_warning)
stream = tweepy.Stream(auth, listener)

stream.filter(track=['flutter', 'alteryx', 'Elon'], is_async=True)

time.sleep(30)
stream.disconnect()


