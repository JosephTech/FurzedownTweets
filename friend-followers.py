#!/usr/bin/python
# -*- coding: utf-8 -*-

import tweepy
import os
import ConfigParser
import inspect

path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

# read config
config = ConfigParser.SafeConfigParser()
config.read(os.path.join(path, "config"))

# create bot
auth = tweepy.OAuthHandler(config.get("twitter","consumer_key"), config.get("twitter","consumer_secret"))
auth.set_access_token(config.get("twitter","access_token"), config.get("twitter","access_token_secret"))
api = tweepy.API(auth)

def get_diff(list1,list2):
    """Outputs objects which are in list1 but not list 2"""
    return list(set(list1).difference(set(list2)))

friend_ids = []
follower_ids = []

print "Fetching Followers..."
for follower in tweepy.Cursor(api.followers).items():
    follower_ids.append(follower.id)

print "Fetching Friends..."
for friend in tweepy.Cursor(api.friends).items():
    friend_ids.append(friend.id)
	
follow_list = get_diff(follower_ids, friend_ids)

print "about to FOLLOW %s people." % len(follow_list)

for user in follow_list:
    try:
        api.create_friendship(user)
    except:
        print "error on user: %s" % api.get_user(user).screen_name
    
print "Done\n\n"