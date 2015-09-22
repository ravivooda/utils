#! /usr/bin/python
import tweepy
import Queue
from keys import keys

import time
 
CONSUMER_KEY = keys['consumer_key']
CONSUMER_SECRET = keys['consumer_secret']
ACCESS_TOKEN = keys['access_token']
ACCESS_TOKEN_SECRET = keys['access_token_secret']

print "Logging into Twitter" 
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

print "Success Login \n\n\n\n"

follow_q = []
 
# First get my ollowers
for follower in tweepy.Cursor(api.followers).items():
    my_follower_name = follower.screen_name
    follow_q.append(my_follower_name)

print "My Followers are: "

print follow_q

print "\n\n\n\n\n ====================================== \n\n\n\n\n"

i = 0; 
while len(follow_q) != 0:
    follower_name = follow_q[0]
    print "\n\n Batch: " + str(i)
    for new_follower in tweepy.Cursor(api.followers_ids, screen_name=follower_name).pages():
        print new_follower
        follow_q.extend(new_follower)
        time.sleep(60)
    follow_q.pop(0)
    i = i+1
