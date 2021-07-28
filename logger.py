import application

import logging
import os

class Logger(logging.FileHandler):

	def __init__(self,
		channelName: str,
		printMessages: bool=True, #if true, messages will be logged as well as printed to stdout
		prefs=None, #should be an instance of the prefs object from globals; if None, sensible defaults are used for arguments not passed in
		level=None, #one of the valid levels in Python's logging module
		filePath: str=None, #the path of the log file, not including the file name
		*args, **kwargs
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
		super().__init__(self.fullPath, *args, **kwargs)
		self.level = level
		if self.level is None:
			try:
				self.level = prefs.logLevel
			except AttributeError: #prefs may not be initialized yet
				self.level = "info"
		fileFormatter = logging.Formatter("%(name)s.%(levelname)s at %(asctime)s, line %(lineno)s:\n\t%(message)s", datefmt="%H:%M:%S, %b %d, %Y")
		fileHandler = logging.FileHandler(self.fullPath)
		fileHandler.setFormatter(fileFormatter)
		self._logger = logging.getLogger(self.channelName)
		self._logger.setLevel(getattr(logging, self.level.upper()))
		self._logger.addHandler(fileHandler)
		if printMessages:
			streamHandler = logging.StreamHandler()
			streamHandler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
			self._logger.addHandler(streamHandler)
	
	def info(self, *args, **kwargs):
		self._logger.info(*args, **kwargs)
	
	def warn(self, *args, **kwargs):
		self._logger.warn(*args, **kwargs)
	
	def debug(self, *args, **kwargs):
		self._logger.debug(*args, **kwargs)
	
	def error(self, message, *args, **kwargs):
		self._handleError(message, "error", *args, **kwargs)
	
	def exception(self, message, *args, **kwargs):
		self._handleError(message, "exception", *args, **kwargs)
	
	def critical(self, message, *args, **kwargs):
		self._handleError(message, "critical", *args, **kwargs)
	
	def _handleError(self, message, errorType, *args, **kwargs):
		"""This is here in case we want special error handling in the future, such as an alert, a separate file, etc
		The errorType argument must be one of "error" or "critical", since getattr is called on the super class to find the correct function."""
		if errorType not in ["error", "exception", "critical"]:
			raise ValueError("Invalid errorType argument.")
		getattr(self._logger, errorType)(message, *args, **kwargs)
