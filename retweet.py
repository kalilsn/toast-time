# toast time twitter bot
# Kalil Smith-Nuevelle
# 7/31/2015

import tweepy
import sys
import os
import re
import time
import secrets  # Various api keys and other private information
from pushbullet import Pushbullet


# initialize api and authenticate via o-auth. returns tweepy API() object
def tweepy_setup():
    # keys imported from secrets.py
    auth = tweepy.OAuthHandler(secrets.consumer_key, secrets.consumer_secret)
    auth.secure = True
    auth.set_access_token(secrets.access_token, secrets.access_token_secret)

    return tweepy.API(auth)


# retweet any toast-related tweets from people I follow
def retweet_statuses(pattern):
    timeline = tweepy_api.home_timeline(count=1000)

    print "Ran at " + time.strftime("%H:%M:%S")
    print "Retrieved %d statuses\n" % (len(timeline),)

    for status in timeline:
        text = status.text.lower()
        if re.search(pattern, text) and not status.retweeted and not status.user.protected and status.user.id != tweepy_api.me().id:
            tweepy_api.retweet(status.id)
            # push notification to phone about retweets
            phone.push_note("Retweeted " + status.user.name + ":", text)


if __name__ == "__main__":
    # setup pushbullet to send push notifications about tweets to my phone
    # pb_phone defined in secrets.py
    pb = Pushbullet(secrets.pb_key)
    phone = filter(lambda x: x.nickname == secrets.pb_phone, pb.devices)[0]

    pattern = re.compile(u"(\U0001F35E)|(bread)|(toast)", re.UNICODE)

    tweepy_api = tweepy_setup()
    retweet_statuses(pattern)
