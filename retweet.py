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
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.secure = True
    auth.set_access_token(access_token, access_token_secret)

    return tweepy.API(auth)


# retweet any toast-related tweets from people I follow
def retweet_statuses():
    dir = os.path.abspath(os.path.dirname(sys.argv[0]))

    timeline = tweepy_api.home_timeline(count=1000)

    print "Ran at " + time.strftime("%H:%M:%S")
    print "Retrieved %d statuses\n" % (len(timeline),)

    if len(timeline) == 0:
        sys.exit()

    with open(dir + "/regex.p", "rb") as f:
        pattern = pickle.load(f)  # compiled regex object for matching toast related content

    for status in timeline:
        text = status.text.lower()
        if re.search(pattern, text) and not status.retweeted and status.user.id != tweepy_api.me().id:
            tweepy_api.retweet(status.id)
            # push notification to phone about retweets
            phone.push_note("Retweeted " + status.user.name + ":", text)

if __name__ == "__main__":
    # setup pushbullet to send push notifications about tweets to my phone
    # pb_phone defined in secrets.py
    pb = Pushbullet(pb_key)
    phone = filter(lambda x: x.nickname == pb_phone, pb.devices)[0]

    tweepy_api = tweepy_setup()
    
    retweet_statuses()

    with open(toaster.make_toast(), "rb") as toast:
        tweepy_api.update_with_media("toast.png", "it's toast time!", file=toast)

        file_data = pb.upload_file(toast, "toast.png")
        phone.push_file(**file_data)
