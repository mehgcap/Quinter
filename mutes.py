import globals
from logger import Logger

import html

class Mute:
	"""
	This is the parent class for tweet mutes. It is not intended to be used directly.
	To make a specific kind of mute, use one of the child classes below. Each child class should implement shouldMuteTweet()
	"""
	
	TYPE_CLIENT = "client"
	TYPE_HASHTAG = "hashtag"
	TYPE_USER = "user"

	def __init__(self, type, value):
		self.logger = Logger(self.__class__, prefs=globals.prefs)
		self.type = type
		self.value = value
	
	def shouldMuteTweet(self, tweet):
		raise NotImplementedError
	
	def toJSON(self):
		return {"type": self.type, "value": self.value}
	
	def __str__(self):
		return f"{self.type}: {self.value}"
	
	def __eq__(self, otherMute) -> bool:
		return self.type == otherMute.type and self.value == otherMute.value

class ClientMute(Mute):

	def __init__(self, value):
		super(ClientMute, self).__init__(self.TYPE_CLIENT, value)
	
	def shouldMuteTweet(self, tweet)-> bool:
		tweetToProcess = tweet
		if hasattr(tweet, "retweeted_status"):
			tweetToProcess = tweet.retweeted_status
		if hasattr(tweet, "quoted_status"):
			tweetToProcess = tweet.quoted_status
		shouldMute = tweetToProcess.source.lower() == self.value.lower()
		if shouldMute:
			self.logger.debug(f"Muting tweet: tweet source {tweetToProcess.source.lower()} matches mute value {self.value}")
		return shouldMute

class HashtagMute(Mute):

	def __init__(self, value):
		super(HashtagMute, self).__init__(self.TYPE_HASHTAG, value)
	
	def shouldMuteTweet(self, tweet)-> bool:
		tweetToProcess = tweet
		if hasattr(tweet, "retweeted_status"):
			tweetToProcess = tweet.retweeted_status
		if hasattr(tweet, "quoted_status"):
			tweetToProcess = tweet.quoted_status
		if hasattr(tweetToProcess, "extended_tweet") and "full_text" in tweetToProcess.extended_tweet:
			text=html.unescape(tweetToProcess.extended_tweet["full_text"])
		else:
			if hasattr(tweetToProcess, "full_text"):
				text=html.unescape(tweetToProcess.full_text)
			else:
				text=html.unescape(tweetToProcess.text)
		#add a number sign to our value before using it, if we don't already have one
		hashtag = self.value
		if hashtag[0] != "#":
			self.logger.debug("Adding # to the start of our value")
			hashtag = "#" + hashtag
		shouldMute = hashtag in text
		if shouldMute:
			self.logger.debug(f"Muting tweet: {hashtag} is present in tweet text")
		return shouldMute


class UserMute(Mute):

	def __init__(self, value):
		super(UserMute, self).__init__(self.USER, value)
	
	def shouldMuteTweet(self, tweet)-> bool:
		tweetToProcess = tweet
		if hasattr(tweet, "retweeted_status"):
			tweetToProcess = tweet.retweeted_status
		if hasattr(tweet, "quoted_status"):
			tweetToProcess = tweet.quoted_status
		shouldMute = tweetToProcess.user.screen_name.lower() == self.value.lower()
		if shouldMute:
			self.logger.debug(f"Muting tweet: tweet sender {tweetToProcess.user.screen_name} matches mute value {self.value}")
		return shouldMute

#this function takes a type and a value, and uses the type to determine which kind of mute to create
def muteFactory(muteType, muteValue):
	if muteType == Mute.TYPE_CLIENT:
		return ClientMute(muteValue)
	elif muteType == Mute.TYPE_HASHTAG:
		return HashtagMute(muteValue)
	elif muteType == Mute.TYPE_USER:
		return UserMute(muteValue)
	raise Exception(f"Mute type \"{muteType}\" is not supported.")
