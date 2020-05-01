from typing import Callable
import tweepy


class TwitterListener(tweepy.StreamListener):
    def __init__(self, push_tweet: Callable, print_error: Callable,
                 print_warning: Callable):
        super().__init__()
        self.PushTweet = push_tweet
        self.PrintError = print_error
        self.PrintWarning = print_warning

    def on_status(self, status):
        if hasattr(status, 'retweeted_status'):
            return True
        text = status.text
        if status.truncated is True:
            text = status.extended_tweet['full_text']
        self.PushTweet(status.author.screen_name, text, status.created_at)
        return True

    def on_error(self, status_code):
        if status_code == 420:
            self.PrintError('Received 420 error from Twitter.  Disconnecting...')
            return False

        self.PrintWarning('Received {status} error from Twitter.  Retrying...'.format(status=status_code))
        return True

    def on_warning(self, notice):
        self.PrintWarning('{code}: {message}'.format(code=notice.code, message=notice.message))
        return True

    def on_disconnect(self, notice):
        self.PrintError('Disconnect code {code}: {reason}'.format(code=notice.code, reason=notice.reason))
        return False
