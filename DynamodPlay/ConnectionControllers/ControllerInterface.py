from abc import ABC, abstractmethod

########################################################################
class ControllerInterface(ABC):

	#----------------------------------------------------------------------
	@abstractmethod
	def getKey():
		pass

	#----------------------------------------------------------------------
	@abstractmethod
	def getStatus():
		pass

	#----------------------------------------------------------------------
	@abstractmethod
	def handleRequest():
		pass

	#----------------------------------------------------------------------
	@abstractmethod
	def setHandlerMap():
		pass