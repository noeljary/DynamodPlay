from threading import Thread

from ConnectionControllers.Player import PlayerController
from ConnectionControllers.Volume import VolumeController
from Queue                        import Queue

########################################################################
class ConnectionHandler(Thread):

	#----------------------------------------------------------------------
	def __init__(self):
		Thread.__init__(self)

		self.handlers = [PlayerController(), VolumeController()]

		self.start()

	#----------------------------------------------------------------------
	def run(self):
		while True:
			req = Queue.get("RECV")
			print("Request: {}".format(req))

			for key in req.keys():
				for handler in self.handlers:
					if key == handler.getKey():
						handler.handleRequest(req[key])

				if key == "REQ":
					self.getStatus()

	#----------------------------------------------------------------------
	def getStatus(self):
		for handler in self.handlers:
			Queue.add("SEND", handler.getStatus())