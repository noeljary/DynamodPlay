from ConnectionControllers.ControllerInterface import ControllerInterface
from Players.Airplay   import AirplayPlayer
from Players.Bluetooth import BluetoothPlayer
from Players.Network   import NetworkPlayer
from Players.Radio     import RadioPlayer
from Queue             import Queue

########################################################################
class PlayerController(ControllerInterface):

	_instance = None

	key       = "PLAYER"

	#----------------------------------------------------------------------
	def __new__(cls):
		if cls._instance is None:
			cls._instance = super(PlayerController, cls).__new__(cls)

			# Set Player List and Default Active Player
			cls.player_list   = [AirplayPlayer(), BluetoothPlayer(), NetworkPlayer(), RadioPlayer()]
			cls.active_player = NetworkPlayer()

			# Set Handler Mapping
			cls.setHandlerMap(cls)

		return cls._instance

	#----------------------------------------------------------------------
	def browse(self, browse):
		return {"BROWSE": self.getPlayer(browse["PLAYER"]).getBrowser().handleRequest(browse), "PLAYER": browse["PLAYER"]}

	#----------------------------------------------------------------------
	def getActivePlayer(self):
		return self.active_player

	#----------------------------------------------------------------------
	def getKey(self):
		return self.key

	#----------------------------------------------------------------------
	def getPlayer(self, key):
		for player in self.player_list:
			if key == player.getKey():
				return player

	#----------------------------------------------------------------------
	def getStatus(self):
		player_statuses = []

		for player in self.player_list:
			player_statuses.append({player.getKey(): player.getStatus()})
		
		return {"PLAYERS": player_statuses}

	#----------------------------------------------------------------------
	def handleRequest(self, data):
		for key in data.keys():
			for mapping in self.request_map:
				if key == mapping["CODE"]:
					if mapping["ARGS"]:
						# TODO: This is ugly AF
						if mapping["SELF"]:
							Queue.add("SEND", {self.getKey(): mapping["FUNC"](self, data[key])})
						else:
							Queue.add("SEND", {self.getKey(): mapping["FUNC"](data[key])})
					else:
						Queue.add("SEND", {self.getKey(): mapping["FUNC"]()})

	#----------------------------------------------------------------------
	def setActivePlayer(self, player):
		# Stop Anything Playing in Active Player
		self.getActivePlayer().stop()

		# Set New Player as Active
		self.active_player = player

	#----------------------------------------------------------------------
	def setHandlerMap(self):
		self.request_map = [
			{"CODE": "LOAD",     "FUNC": self.getActivePlayer(self).load,     "ARGS": True,  "SELF": False},
			{"CODE": "PLAY",     "FUNC": self.getActivePlayer(self).play,     "ARGS": True,  "SELF": False},
			{"CODE": "NEXT",     "FUNC": self.getActivePlayer(self).next,     "ARGS": False, "SELF": False},
			{"CODE": "PREV",     "FUNC": self.getActivePlayer(self).prev,     "ARGS": False, "SELF": False},
			{"CODE": "FFORWARD", "FUNC": self.getActivePlayer(self).fforward, "ARGS": True,  "SELF": False},
			{"CODE": "REWIND",   "FUNC": self.getActivePlayer(self).reverse,  "ARGS": True,  "SELF": False},
			{"CODE": "SHUFFLE",  "FUNC": self.getActivePlayer(self).shuffle,  "ARGS": True,  "SELF": False},
			{"CODE": "REPEAT",   "FUNC": self.getActivePlayer(self).repeat,   "ARGS": True,  "SELF": False},
			{"CODE": "BROWSE",   "FUNC": self.browse,                         "ARGS": True,  "SELF": True}
		]
