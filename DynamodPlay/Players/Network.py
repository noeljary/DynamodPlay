from Audio.Vlc               import Vlc
from Browsers.Plex           import PlexBrowser
from Config                  import Config
from Players.PlayerInterface import PlayerInterface
from Players.PlayProgress    import PlayProgress

########################################################################
class NetworkPlayer(PlayerInterface):

	_instance = None
	key       = "NETWORK"

	#----------------------------------------------------------------------
	def __new__(cls):
		if cls._instance is None:
			cls._instance = super(NetworkPlayer, cls).__new__(cls)

			cls.browsers  = [PlexBrowser()]
			cls.setBrowser(cls, Config.get(cls.getKey(cls), "BROWSER"))

			cls.players   = [Vlc]
			cls.setPlayer(cls, Config.get(cls.getKey(cls), "PLAYER"))

			cls.status    = {"TRACK": None, "PATH": {}, "OFFSET": 0, "TIMER_THREAD": None, "SHUFFLE": False, "REPEAT": False}

		return cls._instance

	#----------------------------------------------------------------------
	def fforward(self):
		return

	#----------------------------------------------------------------------
	def getBrowser(self):
		return self.browser

	#----------------------------------------------------------------------
	def getKey(self):
		return self.key

	#----------------------------------------------------------------------
	def getPlayStream(self):
		return self.status["TRACK"].getStream(self.status["OFFSET"])

	#----------------------------------------------------------------------
	def getPlayer(self):
		return self.player

	#----------------------------------------------------------------------
	def getRepeat(self):
		return self.status["REPEAT"]

	#----------------------------------------------------------------------
	def getShuffle(self):
		return self.status["SHUFFLE"]

	#----------------------------------------------------------------------
	def getStatus(self):
		return

	#----------------------------------------------------------------------
	def getTrackInfo(self, track):
		return {}

	#----------------------------------------------------------------------
	def load(self, load):
		# Check for Offset
		self.status["OFFSET"] = 0 if "OFFSET" not in load.keys() else load["OFFSET"]

		# Get Track Object from Media Hierarchy IDs
		self.status["PATH"]  = load["TRACK"]
		self.status["TRACK"] = self.getBrowser().findMedia(load["TRACK"])

		# Create Player Instance and Start Playing
		self.player_instance = self.player(self.getPlayStream())
		self.play(True)

		# Get Track Information for Display
		metadata = self.getTrackInfo(self.status["TRACK"])

		return {"LOAD": {"PLAYER": self.getKey(), "IS_PLAYING": self.player_instance.isPlaying(), "METADATA": metadata}}

	#----------------------------------------------------------------------
	def next(self):
		return

	#----------------------------------------------------------------------
	def play(self, play):
		if play:
			# Play
			self.player_instance.play()

			# Start Progress Timer Thread
			self.status["TIMER_THREAD"] = PlayProgress(self.status["TRACK"].getRawDuration(), self.status["OFFSET"],
				playing       = self.getPlayStream(),
				callback      = self.updateClient,
				is_playing    = self.player_instance.isPlaying,
				whats_playing = self.getPlayStream
			)
		else:
			# End Timer Thread
			self.status["TIMER_THREAD"].terminate()

			# Pause
			self.player_instance.pause()

		return {"PLAY": {"PLAYER": self.getKey(), "IS_PLAYING": self.player_instance.isPlaying()}}

	#----------------------------------------------------------------------
	def prev(self):
		return

	#----------------------------------------------------------------------
	def repeat(self, repeat):
		self.status["REPEAT"] = repeat
		return {"PLAY": {"PLAYER": self.getKey(), "REPEAT": self.status["REPEAT"]}}

	#---------------------------------------------------------------------
	def reverse(self):
		return

	#----------------------------------------------------------------------
	def setBrowser(self, browser_key):
		for browser in self.browsers:
			if browser_key == browser.getKey():
				browser.setup()
				self.browser = browser

	#----------------------------------------------------------------------
	def setPlayer(self, player_key):
		for player in self.players:
			if player_key == player.getKey():
				self.player = player

	#----------------------------------------------------------------------
	def shuffle(self, shuffle):
		self.status["SHUFFLE"] = shuffle
		return {"PLAY": {"PLAYER": self.getKey(), "SHUFFLE": self.status["SHUFFLE"]}}

	#----------------------------------------------------------------------
	def updateClient(self, progress):
		print(progress)
		self.status["OFFSET"] = progress
		return
