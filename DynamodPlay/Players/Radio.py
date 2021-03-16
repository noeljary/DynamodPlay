from Browsers.Radio          import RadioBrowser
from Config                  import Config
from Players.PlayerInterface import PlayerInterface

########################################################################
class RadioPlayer(PlayerInterface):

	_instance = None
	key       = "RADIO"
	browser   = None

	#----------------------------------------------------------------------
	def __new__(cls):
		if cls._instance is None:
			cls._instance = super(RadioPlayer, cls).__new__(cls)

			cls.browsers   = [RadioBrowser()]
			cls.setBrowser(cls, Config.get(cls.getKey(cls), "BROWSER"))

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
	def getStatus(self):
		return

	#----------------------------------------------------------------------
	def load(self):
		return

	#----------------------------------------------------------------------
	def next(self):
		return

	#----------------------------------------------------------------------
	def play(self, play):
		return

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
	def shuffle(self, shuffle):
		return