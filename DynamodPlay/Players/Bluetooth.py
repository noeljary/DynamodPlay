from Players.PlayerInterface import PlayerInterface

########################################################################
class BluetoothPlayer(PlayerInterface):

	_instance = None
	key       = "BLUETOOTH"

	#----------------------------------------------------------------------
	def __new__(cls):
		if cls._instance is None:
			cls._instance = super(BluetoothPlayer, cls).__new__(cls)

		return cls._instance

	#----------------------------------------------------------------------
	def fforward(self):
		return

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
	def shuffle(self, shuffle):
		return

	#----------------------------------------------------------------------
	def updateClientProg(self, progress):
		return
