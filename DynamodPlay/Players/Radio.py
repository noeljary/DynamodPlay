import datetime

from Audio.Vlc                  import Vlc
from Browsers.Radio             import RadioBrowser
from Config                     import Config
from Media.Metadata.RadioStream import RadioStream
from Players.PlayerInterface    import PlayerInterface
from Players.PlayProgress       import PlayProgress
from Queue                      import Queue

########################################################################
class RadioPlayer(PlayerInterface):

	_instance = None
	key       = "RADIO"

	#----------------------------------------------------------------------
	def __new__(cls):
		if cls._instance is None:
			cls._instance = super(RadioPlayer, cls).__new__(cls)

			cls.browsers  = [RadioBrowser()]
			cls.setBrowser(cls, Config.get(cls.getKey(cls), "BROWSER"))

			cls.players   = [Vlc]
			cls.setPlayer(cls, Config.get(cls.getKey(cls), "PLAYER"))

			cls.metadata  = [RadioStream]

			cls.status    = {"STATION": None, "METADATA": {"ARTIST": None, "TRACK": None, "TITLE": None, "IMG": None}, "METADATA_THREAD": None, "TIMER_THREAD": None, "OPTIONS": ["XFER", "BCAST"]}

		return cls._instance

	#----------------------------------------------------------------------
	def fforward(self, forward):
		return False

	#----------------------------------------------------------------------
	def getBrowser(self):
		return self.browser

	#----------------------------------------------------------------------
	def getMetadataParser(self, metadata_type):
		for parser in self.metadata:
			if parser.getKey() == metadata_type:
				return parser

	#----------------------------------------------------------------------
	def getKey(self):
		return self.key

	#----------------------------------------------------------------------
	def getStatus(self):
		return

	#----------------------------------------------------------------------
	def load(self, load, station = None):
		if station:
			self.status["STATION"] = station
		else:
			# Get Station by Key
			self.status["STATION"] = self.getBrowser().getStation(load["STATION"])

		# Create Player Instance and Start Playing
		self.player_instance  = self.player(self.status["STATION"].getStream())
		self.play(True) 

		return {"LOAD": {"PLAYER": self.getKey(), "METADATA": {"TITLE1": self.status["STATION"].getName(), "IMG": self.status["STATION"].getImg()}, "IS_PLAYING": self.player_instance.isPlaying(), "OPTIONS": self.status["OPTIONS"]}}
	
	#----------------------------------------------------------------------
	def next(self):
		# Stop Current Play
		self.play(False)
		
		# Find Next Station in List
		new_station = self.getBrowser().getNextStation(self.status["STATION"])

		# If Next Station Available - Load
		if new_station:
			return self.load(None, new_station)

	#----------------------------------------------------------------------
	def play(self, play):
		if not self.player_instance:
			return

		if play and not self.player_instance.isPlaying():
			# Play
			self.player_instance.play()

			# Start Metadata Thread
			parser_cls = self.getMetadataParser(self.status["STATION"].getMetadataType())
			if parser_cls:
				self.status["METADATA_THREAD"] = parser_cls(
					station       = self.status["STATION"],
					update_client = self.updateClientMeta,
					is_playing    = self.player_instance.isPlaying
				)

			# Start Progress Timer Thread
			self.status["TIMER_THREAD"] = PlayProgress(0, 0,
				update_client = self.updateClientProg,
				is_playing    = self.player_instance.isPlaying
			)
			
		elif not play and self.player_instance.isPlaying():
			# End Timer Thread
			self.status["TIMER_THREAD"].terminate()

			# End Metadata Thread
			self.status["METADATA_THREAD"].terminate()

			# Pause
			self.player_instance.stop()

		return {"PLAY": {"PLAYER": self.getKey(), "IS_PLAYING": self.player_instance.isPlaying()}}

	#----------------------------------------------------------------------
	def prev(self):
		# Stop Current Play
		self.play(False)

		# Find Previous Station in List
		new_station = self.getBrowser().getPrevStation(self.status["STATION"])

		# If Previous Station Available - Load
		if new_station:
			return self.load(None, new_station)

	#----------------------------------------------------------------------
	def repeat(self, repeat):
		return {"PLAY": {"PLAYER": self.getKey(), "SHUFFLE": False, "REPEAT": False}}

	#----------------------------------------------------------------------
	def reverse(self, reverse):
		return False

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
		return {"PLAY": {"PLAYER": self.getKey(), "SHUFFLE": False, "REPEAT": False}}

	#----------------------------------------------------------------------
	def updateClientMeta(self, artist = None, track = None, title = None, img = None):
		metadata = {}

		if not artist == self.status["METADATA"]["ARTIST"]:
			self.status["METADATA"]["ARTIST"] = artist
			metadata["TITLE2"]                = artist

		if not track == self.status["METADATA"]["TRACK"]:
			self.status["METADATA"]["TRACK"]  = track
			metadata["TITLE1"]                = track
		
		if not title == self.status["METADATA"]["TITLE"]:
			self.status["METADATA"]["TITLE"]  = title
			metadata["TITLE3"]                = title 

		if not img == self.status["METADATA"]["IMG"]:
			self.status["METADATA"]["IMG"]    = img
			metadata["IMG"]                   = img

		if metadata:
			Queue.add("SEND", {"PLAYER": {"LOAD": {"METADATA": metadata}}})

	#----------------------------------------------------------------------
	def updateClientProg(self, progress):
		# Get Display Friendly Progress Value		
		progress_formatted = datetime.datetime.fromtimestamp(progress / 1000).strftime("%H:%M:%S" if progress >= 3600000 else "%M:%S")

		Queue.add("SEND", {"PLAYER": {"PROGRESS": {"POSITION": progress_formatted, "PERCENTAGE": 100, "DURATION": "--:--"}}})
