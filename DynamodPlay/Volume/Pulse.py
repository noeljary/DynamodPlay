from pulsectl import Pulse

from Volume.VolumeInterface import VolumeInterface

########################################################################
class PulseAudio(VolumeInterface):

	agent = "PULSE"

	#---------------------------------------------------------------------------
	def __init__(self):
		self.pulse = Pulse("DynamodPlay")
		self.sink  = self.pulse.sink_list()[0]

	#---------------------------------------------------------------------------
	def getAgent(self):
		return self.agent

	#---------------------------------------------------------------------------
	def getVolumeObj(self):
		return self.sink.volume

	#---------------------------------------------------------------------------
	def getVolume(self):
		return round(self.getVolumeObj().value_flat * 100)

	#---------------------------------------------------------------------------
	def isMuted(self):
		return self.sink.mute

	#---------------------------------------------------------------------------
	def mute(self, mute):
		self.pulse.mute(self.sink, mute)
		return self.isMuted()

	#---------------------------------------------------------------------------
	def setVolume(self, vol):
		vol_obj = self.getVolumeObj()
		vol_obj.value_flat = vol / 100
		self.pulse.volume_set(self.sink, vol_obj)

		if self.isMuted():
			self.mute(False)

		return self.getVolume()