#! /usr/bin/python
import tweepy
import Queue
import logging
from keys import keys

import threading
import time
import json

import requests.packages.urllib3

import ereport



logging.basicConfig(filename='bot.log',level=logging.DEBUG)

# DISABLE OTHER USELESS LOGGING
logging.getLogger("requests").setLevel(logging.CRITICAL)
logging.getLogger("urllib3").setLevel(logging.CRITICAL)
logging.getLogger("oauthlib").setLevel(logging.CRITICAL)
logging.getLogger("tweepy").setLevel(logging.CRITICAL)
logging.getLogger("requests_oauthlib").setLevel(logging.CRITICAL)
requests.packages.urllib3.disable_warnings()


logging.info ('''\n\n\n\n\n\n\n\n
=========================================================================================================================================================================================================
|                                                                               STARTING THE BOT. THIS IS A NEW CYCLE                                                                                   |
=========================================================================================================================================================================================================
''')

CONSUMER_KEY = keys['consumer_key']
CONSUMER_SECRET = keys['consumer_secret']
ACCESS_TOKEN = keys['access_token']
ACCESS_TOKEN_SECRET = keys['access_token_secret']

logging.info("Logging into Twitter" )
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

logging.info("Logged in Successfully\n\n")

follow_q = []
 
# First try get my followers
try:
    for follower in tweepy.Cursor(api.followers).items():
        my_follower_name = follower.id
        follow_q.append(my_follower_name)
except tweepy.TweepError:
    logging.error("Rate limit exceeded. So just putting in my id: " + str(api.me().id) + "\n\n")
    follow_q.append(api.me().id)

followed_q = {}

i = 0;
j = 0;
z = 0;
l = 0;
me = api.me()
logging.info("Well this is my data: " + str(me) + "\n\n")

formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
# mail logger
mlogger = logging.getLogger('mail_logger')
hdlr = logging.FileHandler('mail.log')
hdlr.setFormatter(formatter)
mlogger.addHandler(hdlr)

def send_stats():
    message = "Batch Count: " + str(i) + "\n"
    message+= "Followers touched: " + str(j) + "\n"
    message+= "Bot retouched: " + str(z) + "\n"
    message+= "Error occurred: " + str(l) + "\n"
    if ereport.send_email(message=message):
        mlogger.info("Mail was sent successfully")
    else:
        mlogger.error("MAIL FAILED!!!")
    threading.Timer(10, send_stats).start()
    mlogger.info("Sleeping now")

send_stats()
    

logging.info("Starting the actual bot")
while len(follow_q) != 0:
    try:
        follower_name = follow_q[0]
        logging.info("=====================================================================") #This is the divider for each batch
        logging.info("Batch: " + str(i))
        logging.info("Getting followers for user: " + str(follower_name))
        for new_follower in tweepy.Cursor(api.followers_ids, id=follower_name).pages():
            for new_follower_id in new_follower:
                logging.info("-------------------------------------------------------------------") #This is the divider for iterating through each of the follewers of the user
                logging.info("User ID: " + str(new_follower_id))
                logging.info("Follow Queue List Length: " + str(len(follow_q)))
                logging.info("Followed Queue List Length: " + str(len(followed_q)))

                if new_follower_id in followed_q:
                    logging.info("Current user: " + str(new_follower_id) + " was already followed by the bot in this instance. Skipping for next guy immediately!")
                    z = z+1
                    continue
                    
                followed_q[new_follower_id] = True

                if new_follower_id == me.id: # api.exists_friendship(me,new_follower_id):
                    logging.info("Just me: " + str(new_follower_id) + ". Skipping for the next guy immediately!")
                    continue
                
                #logging.info("Friendship Data:\n" + api.show_friendship(target_id=new_follower_id))
                try:
                    api.create_friendship(new_follower_id)
                    logging.info("Successfully followed user: " + str(new_follower_id))
                except tweepy.TweepError as e:
                    logging.error("Unable to follow user: " + str(new_follower_id))
                    logging.error(e)
                    l=l+1;
                if new_follower_id not in follow_q:
                    logging.info("Added current user: " + str(new_follower_id) + " to my queue")
                    follow_q.append(str(new_follower_id))
                else:
                    logging.info("Already traversed loop with user: " + str(new_follower_id) + ". Not adding to queue")
                time.sleep(60)
                j = j+1
        follow_q.pop(0)
        i = i+1
    except Exception as e:
        logging.error("Got an exception in the outer most loop")
        logging.error(e)
        time.sleep(10)
logging.info("REACHED END OF THE LOOP, GOODBYE")
