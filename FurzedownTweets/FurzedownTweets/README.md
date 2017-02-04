FurzedownTweets
===============

Raspberry Pi powered TwitterBot project using Python

Polls for hashtag #furzedown and retweets any found via @FurzedownTweets

https://twitter.com/furzedowntweets

Exceptions are: 
- retweets
- starts with @username
- status words in wordBlackList
- status user in userBlackList

Based on https://github.com/basti2342/retweet-bot, plus updated version of Tweepy from https://github.com/knowsis/tweepy to fix issue (https://github.com/basti2342/retweet-bot/issues/2)

Currently running on Raspberry Pi (raspbian) via crontab:
- retweet.py: every 15 minutes
- friend-followers.py - every day at midnight

Features under development
- review and refactor code
