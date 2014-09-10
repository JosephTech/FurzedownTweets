#!/usr/bin/python
# -*- coding: utf-8 -*-

import tweepy
import os
import ConfigParser
import inspect

#path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

# read config
config = ConfigParser.ConfigParser()
config.read("/home/pi/jules/retweet/furzedown/config")

# your hashtag or search query and tweet language (empty = all languages)
hashtag = config.get("settings","search_query")
tweetLanguage = config.get("settings","tweet_language")

# blacklisted users and words
userBlacklist = ["companieslist","tootinkstudio","wwwfantasylondo","companieslist","babeinshorts99","PhoneSexHoneyUK","PropertyInfo_UK","HS_EstateAgents","YinGyanGgirls","xxxdenisexxx1","WellKell","tonya20011","superwilliam1","stevejobsworth1","Spazmataz1","SixOfSade","sharontweedy1","SharleneDEMTWO","Sexy_IshaPD","sassychicchar","PropertyWizzUK","OneSiobhan","MelanieSousaLDN","LauraLaurs1","krystalmeth5","JoanneSWID", "kateWinsAll"]
wordBlacklist = ["RT", u"♺", "cunt", "fuck", "fucking","Harrison Sellars","EstateAgents"]

# build savepoint path + file
lastid = long(config.get("twitter","lastid"))
#print lastid
#last_id_filename = "last_id_hashtag_furzedown"
#rt_bot_path = os.path.dirname(os.path.abspath(__file__))
#last_id_file = os.path.join(rt_bot_path, last_id_filename)



# create bot
#print "create bot"
auth = tweepy.OAuthHandler(config.get("twitter","consumer_key"), config.get("twitter","consumer_secret"))
auth.set_access_token(config.get("twitter","access_token"), config.get("twitter","access_token_secret"))
api = tweepy.API(auth)

# retrieve last savepoint if available
#try:
#	with open(last_id_file, "r") as file:
#		savepoint = file.read()
#except IOError:
#	savepoint = ""
#	print "No savepoint found. Trying to get as many results as possible."

# search query
#print "timelineiterator"
timelineIterator = tweepy.Cursor(api.search, q=hashtag, since_id=lastid, lang=tweetLanguage).items()

# put everything into a list to be able to sort/filter
timeline = []
for status in timelineIterator:
	timeline.append(status)

print "Found %d tweets" % (len(timeline))

try:
    last_tweet_id = long(timeline[0].id)	
except IndexError:
    last_tweet_id = lastid

#print type(timeline[0].id)

# filter @replies/blacklisted words & users out and reverse timeline
timeline = filter(lambda status: status.text[0] != "@", timeline)
timeline = filter(lambda status: not any(word in status.text.split() for word in wordBlacklist), timeline)
timeline = filter(lambda status: status.author.screen_name not in userBlacklist, timeline)
timeline.reverse()

tw_counter = 0
err_counter = 0

# iterate the timeline and retweet
for status in timeline:
	try:
		#only allow tweets with 3 or less hashtags
		str = status.text
		search = "#"
		hashTagCount = str.count(search)
		if hashTagCount <= 3:
			print "(%(date)s) %(name)s: %(message)s\n" % \
				{ "date" : status.created_at,
				"name" : status.author.screen_name.encode('utf-8'),
				"message" : status.text.encode('utf-8') }	
				
			api.retweet(status.id)
			tw_counter += 1
	except tweepy.error.TweepError as e:
		# just in case tweet got deleted in the meantime or already retweeted
		print e
                err_counter += 1
		continue


message =  "Finished. %d Tweets retweeted, %d errors occured." % (tw_counter, err_counter)
print(message)
api.send_direct_message(screen_name="julesjoseph", text=message)

# write last retweeted tweet id to file
#print str(last_tweet_id)
#with open(last_id_file, "w") as file:
#	file.write(str(last_tweet_id))
#print type(last_tweet_id)
#print str(last_tweet_id)

#configTweetId = str(last_tweet_id)
#print configTweetId
config.set("twitter","lastid",last_tweet_id)
with open("config", "wb") as configfile:
	config.write(configfile)

