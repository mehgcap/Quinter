import application
from logger import Logger
import platform
import sys

def customExceptHook(exceptionType, exceptionValue, exceptionTraceback):
	logger = Logger("global exceptHook", True, "info", "")
	logger.critical(f"An unhandled error was raised.\n{exceptionType}: {exceptionValue}\nTraceback: {exceptionTraceback}")

sys.excepthook = customExceptHook
sys.dont_write_bytecode=True
import shutil
import os
if os.path.exists(os.path.expandvars("%temp%\gen_py"))==True:
	shutil.rmtree(os.path.expandvars("%temp%\gen_py"))
# Bye foo!
import wx
app = wx.App(redirect=False)

import speak
from GUI import main
import globals
globals.load()
if globals.prefs.window_shown==True:
	main.window.Show()
else:
	speak.speak("Welcome to Quinter! Main window hidden.")
import utils
app.MainLoop()
