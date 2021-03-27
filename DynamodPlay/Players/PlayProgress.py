import time

from datetime  import datetime
from datetime  import timedelta
from threading import Thread

from Config    import Config

########################################################################
class PlayProgress(Thread):

	#----------------------------------------------------------------------
	def __init__(self, duration, offset, update_client = None, is_playing = None, is_complete = None):
		Thread.__init__(self)
		
		# Setup Timer Configs
		self.config       = {"DURATION": timedelta(milliseconds = duration), "OFFSET": timedelta(seconds = offset)}
		self.progress     = timedelta(seconds = 0) + self.config["OFFSET"]
		self.running      = True

		# Links to Parent Player Functions
		self.isPlaying    = is_playing
		self.updateClient = update_client
		self.isComplete   = is_complete

		# How Often to Send Updates to Client
		self.update_freq  = int(Config.get("PLAYER", "UPDATE_FREQUENCY"))

		self.start()

	#----------------------------------------------------------------------
	def run(self):
		while not self.isPlaying():
			time.sleep(0.1)

		while self.isPlaying() and self.running:
			# Rate Limit Cycles
			time.sleep(1 / self.update_freq)

			# Add Update Frequency to Timer Progress
			self.progress += timedelta(seconds = 1 / self.update_freq)

			# Send Update to Callback
			self.updateClient(self.progress.seconds + self.progress.microseconds / 1000000)

		# Move to Next Media Where Possible
		if self.progress + timedelta(seconds = self.update_freq * (1 / self.update_freq)) >= self.config["DURATION"] and self.isComplete:
			self.isComplete()

	#----------------------------------------------------------------------
	def terminate(self):
		self.running = False
