import inspect

from ConnectionControllers.ControllerInterface import ControllerInterface
from Players.Airplay   import AirplayPlayer
from Players.Bluetooth import BluetoothPlayer
from Players.Network   import NetworkPlayer
from Players.PlayerInterface import PlayerInterface
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
			cls.player_list     = [AirplayPlayer(), BluetoothPlayer(), NetworkPlayer(), RadioPlayer()]
			cls.active_player   = NetworkPlayer()

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
					isclass = inspect.isclass(mapping["CLASS"])
					if mapping["ARGS"]:
						args    = (self, data[key]) if isclass else (data[key],)
						Queue.add("SEND", {self.getKey(): getattr(mapping["CLASS"] if isclass else mapping["CLASS"](self), mapping["FUNC"])(*(args))})
					else:
						Queue.add("SEND", {self.getKey(): getattr(mapping["CLASS"] if isclass else mapping["CLASS"](self), mapping["FUNC"])()})

	#----------------------------------------------------------------------
	def setActivePlayer(self, key):
		# Stop Anything Playing in Active Player
		self.getActivePlayer().play(False)

		# Set New Player as Active
		for player in self.player_list:
			if player.getKey() == key:
				self.active_player = player

	#----------------------------------------------------------------------
	def setHandlerMap(self):
		self.request_map = [
			{"CODE": "PLAYER",   "CLASS": self,                 "FUNC": "setActivePlayer", "ARGS": True},
			{"CODE": "BROWSE",   "CLASS": self,                 "FUNC": "browse",          "ARGS": True},
			{"CODE": "LOAD",     "CLASS": self.getActivePlayer, "FUNC": "load",            "ARGS": True},
			{"CODE": "PLAY",     "CLASS": self.getActivePlayer, "FUNC": "play",            "ARGS": True},
			{"CODE": "NEXT",     "CLASS": self.getActivePlayer, "FUNC": "next",            "ARGS": False},
			{"CODE": "PREV",     "CLASS": self.getActivePlayer, "FUNC": "prev",            "ARGS": False},
			{"CODE": "FFORWARD", "CLASS": self.getActivePlayer, "FUNC": "fforward",        "ARGS": True},
			{"CODE": "REWIND",   "CLASS": self.getActivePlayer, "FUNC": "reverse",         "ARGS": True},
			{"CODE": "SHUFFLE",  "CLASS": self.getActivePlayer, "FUNC": "shuffle",         "ARGS": True},
			{"CODE": "REPEAT",   "CLASS": self.getActivePlayer, "FUNC": "repeat",          "ARGS": True}
		]
