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
	def fforward(self, forward):
		# Stop Current Play
		self.play(False)

		# Check Durations
		track = self.getPlayTrack()

		if self.status["OFFSET"] + (forward / 1000) < track.getRawDuration():
			# Play from New Offset
			self.load(None, track, self.status["OFFSET"] + (forward / 1000))
		else:
			# Play Next
			self.next()

	#----------------------------------------------------------------------
	def getBrowser(self):
		return self.browser

	#----------------------------------------------------------------------
	def getKey(self):
		return self.key

	#----------------------------------------------------------------------
	def getPlayTrack(self):
		return self.status["PATH"][len(self.status["PATH"]) - 1]

	#----------------------------------------------------------------------
	def getPlayTrackParent(self):
		return self.status["PATH"][len(self.status["PATH"]) - 2]

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
	def load(self, load, track = None, offset = 0):
		if track:
			self.status["OFFSET"] = offset
			self.status["PATH"][len(self.status["PATH"]) - 1] = track
		else:
			# Check for Offset
			self.status["OFFSET"] = 0 if "OFFSET" not in load.keys() else load["OFFSET"]

			# Get Track Object from Media Hierarchy IDs
			self.status["PATH"] = self.getBrowser().findMedia(load["TRACK"])
			track = self.getPlayTrack()

		# Create Player Instance and Start Playing
		self.player_instance = self.player(track.getStream(self.status["OFFSET"]))
		self.play(True)

		# Get Track Information for Display
		metadata = self.getTrackInfo(track)

		return {"LOAD": {"PLAYER": self.getKey(), "IS_PLAYING": self.player_instance.isPlaying(), "METADATA": metadata}}

	#----------------------------------------------------------------------
	def next(self):
		print("Calling Next")

		# Stop Current Play
		self.play(False)

		# Get Current Track Details
		old_track    = self.getPlayTrack()
		track_parent = self.getPlayTrackParent()

		# Select New Track
		if self.status["SHUFFLE"]:
			new_track = track_parent.getTrackRnd()
		elif self.status["REPEAT"]:
			new_track = old_track
		else:
			new_track = track_parent.getTrackNext(old_track)

		print("New Track: {}".format(new_track.toDict()))
		# Load New Track
		if new_track:
			self.load(None, new_track)

	#----------------------------------------------------------------------
	def play(self, play):
		if play and not self.player_instance.isPlaying():
			# Play
			self.player_instance.play()

			# Start Progress Timer Thread
			track = self.status["PATH"][len(self.status["PATH"]) - 1]
			self.status["TIMER_THREAD"] = PlayProgress(track.getRawDuration(), self.status["OFFSET"],
				update_client = self.updateClient,
				is_playing    = self.player_instance.isPlaying,
				is_complete   = self.next
			)
		elif not play and self.player_instance.isPlaying():
			# End Timer Thread
			self.status["TIMER_THREAD"].terminate()

			# Pause
			self.player_instance.pause()

		return {"PLAY": {"PLAYER": self.getKey(), "IS_PLAYING": self.player_instance.isPlaying()}}

	#----------------------------------------------------------------------
	def prev(self):
		# Stop Current Play
		self.play(False)

		# Get Track Details
		old_track = self.status["PATH"][len(self.status["PATH"]) - 1]
		track_parent = self.status["PATH"][len(self.status["PATH"]) - 2]

		# Select New Track
		if self.status["SHUFFLE"]:
			new_track = track_parent.getTrackRnd()
		elif self.status["REPEAT"]:
			new_track = old_track
		else:
			new_track = track_parent.getTrackPrev(old_track)

		# Load New Track
		if new_track:
			self.load(None, new_track)

	#----------------------------------------------------------------------
	def repeat(self, repeat):
		self.status["REPEAT"] = repeat

		# Cannot Repeat and Shuffle at the same time
		if repeat and self.status["SHUFFLE"]:
			self.shuffle(False)

		return {"PLAY": {"PLAYER": self.getKey(), "REPEAT": self.status["REPEAT"], "SHUFFLE": self.status["SHUFFLE"]}}

	#---------------------------------------------------------------------
	def reverse(self, reverse):
		# Stop Current Play
		self.play(False)

		# Check Durations
		offset = self.status["OFFSET"] - (reverse / 1000) if self.status["OFFSET"] - (reverse / 1000) > 0 else 0

		# Play from New Offset
		self.load(None, self.getPlayTrack(), offset)

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

		# Cannot Shuffle and Repeat at the same time
		if shuffle and self.status["REPEAT"]:
			self.repeat(False)

		return {"PLAY": {"PLAYER": self.getKey(), "SHUFFLE": self.status["SHUFFLE"], "REPEAT": self.status["REPEAT"]}}

	#----------------------------------------------------------------------
	def updateClient(self, progress):
		print(progress)
		self.status["OFFSET"] = progress
		return
