#!/usr/bin/python

from Config import Config
from Queue  import Queue

from ConnHandler import ConnectionHandler
from WebSock import WebSock

# Run the program
if __name__ == "__main__":
	# Load Configs
	Config.init()

	# Create Send/Recv Queues
	Queue.init()

	# Start WebSocket and Connection Handler
	ConnectionHandler()
	WebSock()
