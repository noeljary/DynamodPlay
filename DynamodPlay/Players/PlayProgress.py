import time

from datetime  import datetime
from datetime  import timedelta
from threading import Thread

from Config    import Config

########################################################################
class PlayProgress(Thread):

	#----------------------------------------------------------------------
	def __init__(self, duration, offset, playing = None, callback = None, is_playing = None, whats_playing = None):
		Thread.__init__(self)
		
		# Setup Timer Configs
		self.config       = {"DURATION": timedelta(seconds = duration), "OFFSET": timedelta(seconds = offset), "PLAYING": playing}
		self.progress     = timedelta(seconds = 0) + self.config["OFFSET"]
		self.running      = True

		# Links to Parent Player Functions
		self.isPlaying    = is_playing
		self.whatsPlaying = whats_playing
		self.updateClient = callback

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

	#----------------------------------------------------------------------
	def terminate(self):
		self.terminate = False
