from Audio.Vlc               import Vlc
from Browsers.Plex           import PlexBrowser
from Config                  import Config
from Players.PlayerInterface import PlayerInterface

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
	def getPlayer(self):
		return self.player

	#----------------------------------------------------------------------
	def getStatus(self):
		return

	#----------------------------------------------------------------------
	def load(self, load):
		track = self.getBrowser().findMedia(load["TRACK"])
		self.player_instance = self.player(track.getStream())
		return {"LOAD": {"PLAYER": self.getKey(), "TRACK": track.getStream(), "IS_PLAYING": self.player_instance.isPlaying()}}

	#----------------------------------------------------------------------
	def next(self):
		return

	#----------------------------------------------------------------------
	def play(self, play):
		if play:
			return {"LOAD": {"PLAYER": self.getKey(), "IS_PLAYING": self.player_instance.play()}}
		else:
			return {"LOAD": {"PLAYER": self.getKey(), "IS_PLAYING": self.player_instance.pause()}}

	#----------------------------------------------------------------------
	def prev(self):
		return

	#----------------------------------------------------------------------
	def repeat(self, repeat):
		return

	#----------------------------------------------------------------------
	def reverse(self):
		return

	#----------------------------------------------------------------------
	def repeat(self, repeat):
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
		return
