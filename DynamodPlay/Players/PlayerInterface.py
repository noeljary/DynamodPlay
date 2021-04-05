from abc import ABC, abstractmethod

########################################################################
class PlayerInterface(ABC):

	#----------------------------------------------------------------------
	@abstractmethod
	def fforward(forward):
		pass

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
	def load():
		pass

	#----------------------------------------------------------------------
	@abstractmethod
	def next():
		pass

	#----------------------------------------------------------------------
	@abstractmethod
	def play(play):
		pass

	#----------------------------------------------------------------------
	@abstractmethod
	def prev():
		pass

	#----------------------------------------------------------------------
	@abstractmethod
	def repeat(repeat):
		pass

	#----------------------------------------------------------------------
	@abstractmethod
	def reverse(reverse):
		pass

	#----------------------------------------------------------------------
	@abstractmethod
	def shuffle(shuffle):
		pass

	#----------------------------------------------------------------------
	@abstractmethod
	def updateClientProg():
		pass
