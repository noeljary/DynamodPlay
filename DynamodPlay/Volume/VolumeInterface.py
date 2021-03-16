from abc import ABC, abstractmethod

########################################################################
class VolumeInterface(ABC):

	#----------------------------------------------------------------------
	@abstractmethod
	def getAgent():
		pass

	#----------------------------------------------------------------------
	@abstractmethod
	def getVolume():
		pass

	#----------------------------------------------------------------------
	@abstractmethod
	def isMuted():
		pass

	#----------------------------------------------------------------------
	@abstractmethod
	def mute():
		pass

	#----------------------------------------------------------------------
	@abstractmethod
	def setVolume(vol):
		pass
