import application

import logging
import os

class Logger(logging.Logger):

	def __init__(self,
		channelName: str,
		printMessages: bool=True, #if true, messages will be printed to stdout as well as logged to a file
		prefs=None, #should be an instance of the prefs object from globals; if None, sensible defaults are used for arguments not passed in
		level=None, #one of the valid levels in Python's logging module
		filePath: str=None, #the path of the log file, not including the file name
		*args,
		**kwargs
	) -> None:
		self.channelName = channelName
		self.filePath = filePath
		if self.filePath is None:
			try:
				self.filePath = prefs.user_config_dir
			except AttributeError:
				self.filePath = "" #should put the log in the main directory
		self.filename = f"{application.shortname}.log"
		self.fullPath = os.path.join(self.filePath, self.filename)
		self.level = level
		if self.level is None:
			try:
				self.level = prefs.logLevel
			except AttributeError: #prefs may not be initialized yet
				self.level = "info"
		self.levelInt = logging._checkLevel(self.level.upper())
		super().__init__(self.channelName, self.levelInt, *args, **kwargs)

		fileFormatter = logging.Formatter("%(name)s.%(levelname)s at %(asctime)s, line %(lineno)s:\n\t%(message)s", datefmt="%H:%M:%S, %b %d, %Y")
		fileHandler = logging.FileHandler(self.fullPath)
		fileHandler.setFormatter(fileFormatter)
		self.addHandler(fileHandler)
		if printMessages:
			streamHandler = logging.StreamHandler()
			streamHandler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
			self.addHandler(streamHandler)

