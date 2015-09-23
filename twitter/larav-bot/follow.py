#! /usr/bin/python
import tweepy
import Queue
from keys import keys

import time
import json

def pretty_print(dict):
    print json.dumps(dict, sort_keys=True, indent=4)
 
CONSUMER_KEY = keys['consumer_key']
CONSUMER_SECRET = keys['consumer_secret']
ACCESS_TOKEN = keys['access_token']
ACCESS_TOKEN_SECRET = keys['access_token_secret']

print "Logging into Twitter" 
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

print "Success Login \n\n\n\n"

pretty_print(api.rate_limit_status())

follow_q = []
 
# First get my ollowers
for follower in tweepy.Cursor(api.followers).items():
    my_follower_name = follower.id
    follow_q.append(my_follower_name)

print "My Followers are: "

print follow_q

print "\n\n\n\n\n ====================================== \n\n\n\n\n"

i = 0; 
me = api.me()
print me
while len(follow_q) != 0:
    follower_name = follow_q[0]
    print "\n\n Batch: " + str(i)
    print "Searching for: " + str(follower_name)
    for new_follower in tweepy.Cursor(api.followers_ids, id=follower_name).pages():
        for new_follower_id in new_follower:
            if new_follower_id == me.id: # api.exists_friendship(me,new_follower_id):
                print "Already friends: " + str(new_follower_id)
                continue
            try:
                api.create_friendship(new_follower_id)
                print "Success Man"
            except tweepy.TweepError as e:
                print e
            print new_follower_id
            follow_q.append(new_follower_id)
            time.sleep(10)
    follow_q.pop(0)
    i = i+1
