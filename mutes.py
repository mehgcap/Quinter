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
		return hasattr(tweet, "source") and tweet.source == self.value

class HashtagMute(Mute):

	def __init__(self, value):
		super(HashtagMute, self).__init__(self.TYPE_HASHTAG, value)
	
	def shouldMuteTweet(self, tweet)-> bool:
		return hasattr(tweet, "text") and self.value in tweet.text


class UserMute(Mute):

	def __init__(self, value):
		super(UserMute, self).__init__(self.USER, value)
	
	def shouldMuteTweet(self, tweet)-> bool:
		return hasattr(tweet, "sender") and self.value in tweet.sender

#this function takes a type and a value, and uses the type to determine which kind of mute to create
def muteFactory(muteType, muteValue):
	if muteType == Mute.TYPE_CLIENT:
		return ClientMute(muteValue)
	elif muteType == Mute.TYPE_HASHTAG:
		return HashtagMute(muteValue)
	elif muteType == Mute.TYPE_USER:
		return UserMute(muteValue)
	raise Exception(f"Mute type \"{muteType}\" is not supported.")
