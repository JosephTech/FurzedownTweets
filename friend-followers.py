
#!/usr/bin/python
# -*- coding: utf-8 -*-

import tweepy
import os
import ConfigParser
import inspect

# read config
config = ConfigParser.ConfigParser()
config.read("/home/pi/jules/retweet/furzedown/config")


# build savepoint path + file
lastuser = config.get("twitter","lastuser")
print lastuser

# create bot
auth = tweepy.OAuthHandler(config.get("twitter","consumer_key"), config.get("twitter","consumer_secret"))
auth.set_access_token(config.get("twitter","access_token"), config.get("twitter","access_token_secret"))
api = tweepy.API(auth)
followers = []

for follower in tweepy.Cursor(api.followers).items(25):
	followers.append(follower)

latestUser = followers[0].screen_name
followers.reverse()
found = False

new_friends = 0
for f in followers:
	if found:
		print "New Friend!"
		print f.screen_name
		new_friends += 1
		api.create_friendship(f.screen_name)
	if f.screen_name == lastuser:
		found = True


message = "Followed back %d friends" % (new_friends)
api.send_direct_message(screen_name="julesjoseph", text=message)

config.set("twitter","lastuser",latestUser)
with open("config","wb") as configfile:
	config.write(configfile)
