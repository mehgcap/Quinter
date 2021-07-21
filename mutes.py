class Mute:
	"""
	This is the parent class for tweet mutes. It is not intended to be used directly.
	To make a specific kind of mute, use one of the child classes below. Each child class should implement shouldMuteTweet()
	"""
	
	TYPE_CLIENT = "client"
	TYPE_HASHTAG = "hashtag"
	TYPE_USER = "user"

	def __init__(self, type, value):
		self.type = type
		self.value = value
	
	def shouldMuteTweet(tweet):
		raise NotImplementedError

class ClientMute(Mute):

	def __init__(self, value):
		super(ClientMute, self).__init__(self.TYPE_CLIENT, value)
	
	def shouldMuteTweet(tweet)-> bool:
		return hasattr(tweet, "source") and tweet.source == self.value

