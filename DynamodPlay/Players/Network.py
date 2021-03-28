import datetime
import re

from Audio.Vlc               import Vlc
from Browsers.Plex           import PlexBrowser
from Config                  import Config
from Media.Album             import Album
from Media.Artist            import Artist
from Media.Library           import Library
from Players.PlayerInterface import PlayerInterface
from Players.PlayProgress    import PlayProgress
from Queue                   import Queue

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

			cls.status    = {"PATH": None, "OFFSET": 0, "TIMER_THREAD": None, "SHUFFLE": False, "REPEAT": False, "OPTIONS": ["SHUFFLE", "REPEAT", "XFER", "BCAST"]}
			cls.re_meta   = re.compile(r"^([A-z]+\s*[0-9]+[\s\-]*)+(.*)$")

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
		status = {"PLAYER": self.getKey(), "OPTIONS": self.status["OPTIONS"]}

		# If Playing or Has Played
		if self.status["PATH"]:
			status["IS_PLAYING"] = self.player_instance.isPlaying()
			status["METADATA"]   = self.getTrackInfo()

		return {"STATUS": status}

	#----------------------------------------------------------------------
	def getTrackInfo(self):
		meta   = {}
		track  = self.getPlayTrack()
		parent = self.getPlayTrackParent()

		# Titles
		title_split = self.re_meta.match(track.getName())

		if not title_split:
			# Probably Music or Radio Play
			meta["TITLE"] = track.getName()
			if isinstance(parent, Album):
				meta["TITLE2"] = parent.getName()
				meta["TITLE3"] = parent.getArtistName()
			elif isinstance(parent, Artist):
				meta["TITLE2"] = parent.getName()
			elif isinstance(parent, Library):
				meta["TITLE2"] = track.getArtistName()
		elif len(title_split.groups()) == 2:
			# Probably Audio Book with Chapter Name
			meta["TITLE"]  = title_split.groups[1]
			meta["TITLE2"] = parent.getName()
			meta["TITLE3"] = parent.getArtistName()
		elif len(title_split.groups()) == 1:
			# Probably Audio Book
			meta["TITLE"] = parent.getName()
			meta["TITLE2"] = parent.getArtistName()			

		# Track X of Y
		meta["TRACK_NUM"]  = parent.getTrackNum(track)
		meta["NUM_TRACKS"] = parent.getNumTracks()

		# Album Art
		meta["IMAGE"] = track.getImg()

		# Playback Progress
		meta["DURATION"]     = track.getDuration()
		meta["RAW_DURATION"] = track.getRawDuration()
		meta["POSITION"]     = datetime.datetime.fromtimestamp(self.status["OFFSET"]).strftime("%H:%M:%S" if self.status["OFFSET"] >= 3600 else "%M:%S")

		return meta

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
		metadata = self.getTrackInfo()

		return {"LOAD": {"PLAYER": self.getKey(), "IS_PLAYING": self.player_instance.isPlaying(), "METADATA": metadata, "OPTIONS": self.status["OPTIONS"]}}

	#----------------------------------------------------------------------
	def next(self):
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
		# Update Player with Playback Progress
		self.status["OFFSET"] = progress

		# Assemble Duration Details
		track              = self.getPlayTrack()
		duration_formatted = track.getDuration()
		duration_raw       = track.getRawDuration()
		progress_formatted = datetime.datetime.fromtimestamp(progress / 1000).strftime("%H:%M:%S" if progress >= 3600000 else "%M:%S")
		percentage_played  = round((progress / duration_raw) * 100, 2)

		Queue.add("SEND", {"PLAYER": {"PROGRESS": {"POSITION": progress_formatted, "PERCENTAGE": percentage_played, "DURATION": duration_formatted, "RAW_DURATION": duration_raw}}})
