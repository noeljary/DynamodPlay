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

			cls.status    = {"PATH": None, "OFFSET": 0, "TIMER_THREAD": None, "SHUFFLE": False, "REPEAT": False}

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
		return self.status["PATH"][len(self.status["PATH"]) - 1].getStream(self.status["OFFSET"])

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
	def load(self, load, track = None):
		if track:
			self.status["OFFSET"] = 0
			self.status["PATH"][len(self.status["PATH"]) - 1] = track
		else:
			# Check for Offset
			self.status["OFFSET"] = 0 if "OFFSET" not in load.keys() else load["OFFSET"]

			# Get Track Object from Media Hierarchy IDs
			self.status["PATH"] = self.getBrowser().findMedia(load["TRACK"])
			track = self.status["PATH"][len(self.status["PATH"]) - 1]

		# Create Player Instance and Start Playing
		self.player_instance = self.player(self.getPlayStream())
		self.play(True)

		# Get Track Information for Display
		metadata = self.getTrackInfo(track)

		return {"LOAD": {"PLAYER": self.getKey(), "IS_PLAYING": self.player_instance.isPlaying(), "METADATA": metadata}}

	#----------------------------------------------------------------------
	def next(self):
		# Stop Current Play
		self.play(False)

		# Get New Track Details
		old_track = self.status["PATH"][len(self.status["PATH"]) - 1]
		track_parent = self.status["PATH"][len(self.status["PATH"]) - 2]
		new_track = track_parent.getTrackNext(old_track)

		# Load New Track
		if new_track:
			self.load(None, new_track)

	#----------------------------------------------------------------------
	def play(self, play):
		if play:
			# Play
			self.player_instance.play()

			# Start Progress Timer Thread
			track = self.status["PATH"][len(self.status["PATH"]) - 1]
			self.status["TIMER_THREAD"] = PlayProgress(track.getRawDuration(), self.status["OFFSET"],
				update_client = self.updateClient,
				is_playing    = self.player_instance.isPlaying,
				is_complete   = self.next
			)
		else:
			# End Timer Thread
			self.status["TIMER_THREAD"].terminate()

			# Pause
			self.player_instance.pause()

		return {"PLAY": {"PLAYER": self.getKey(), "IS_PLAYING": self.player_instance.isPlaying()}}

	#----------------------------------------------------------------------
	def prev(self):
		# Stop Current Play
		self.play(False)

		# Get New Track Details
		old_track = self.status["PATH"][len(self.status["PATH"]) - 1]
		track_parent = self.status["PATH"][len(self.status["PATH"]) - 2]
		new_track = track_parent.getTrackPrev(old_track)

		# Load New Track
		if new_track:
			self.load(None, new_track)

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
