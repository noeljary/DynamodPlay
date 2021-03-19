from ConnectionControllers.ControllerInterface import ControllerInterface
from Volume.Pulse import PulseAudio
from Config       import Config
from Queue        import Queue

########################################################################
class VolumeController(ControllerInterface):

	_instance = None

	key       = "VOLUME"

	#----------------------------------------------------------------------
	def __new__(cls):
		if cls._instance is None:
			cls._instance = super(VolumeController, cls).__new__(cls)

			# Map Audio Agent
			cls.agent_list   = [PulseAudio()]
			agent_cfg = Config.get("VOLUME", "AGENT", "PULSE")
			for agent in cls.agent_list:
				if agent_cfg == agent.getAgent():
					cls.active_agent = agent

			# Exit if No Audio Agent
			if cls.active_agent == None:
				print("COULD NOT START - NO AUDIO AGENT")
				exit(-1)

			# Set Handler Mapping
			cls.setHandlerMap(cls)

		return cls._instance


	#----------------------------------------------------------------------
	def getActiveAgent(self):
		return self.active_agent

	#----------------------------------------------------------------------
	def getKey(self):
		return self.key

	#----------------------------------------------------------------------
	def getStatus(self):
		return {self.getKey(): {"VOLUME": self.getActiveAgent().getVolume(), "MUTE": self.getActiveAgent().isMuted()}}

	#----------------------------------------------------------------------
	def handleRequest(self, data):
		for key in data.keys():
			for mapping in self.request_map:
				if key == mapping["CODE"]:
					Queue.add("SEND", mapping["FUNC"](self, data[key] if mapping["ARGS"] else None))

	#----------------------------------------------------------------------
	def mute(self, mute):
		return {self.getKey(): {"MUTE": self.getActiveAgent().mute(mute)}}

	#----------------------------------------------------------------------
	def setHandlerMap(self):
		self.request_map = [
			{"CODE": "VOLUME", "FUNC": self.setVolume, "ARGS": True},
			{"CODE": "MUTE",   "FUNC": self.mute,      "ARGS": True}
		]

	#----------------------------------------------------------------------
	def setVolume(self, vol):
		return {self.getKey(): {"VOLUME": self.getActiveAgent().setVolume(vol), "MUTE": self.getActiveAgent().isMuted()}}
