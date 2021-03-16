import asyncio
import json
import time
import websockets

from threading import Thread

from Config import Config
from Queue  import Queue

########################################################################
class WebSock(Thread):

	#----------------------------------------------------------------------
	def __init__(self):
		Thread.__init__(self)
		self.sockets = set()
		self.start()

	#----------------------------------------------------------------------
	def run(self):
		asyncio.set_event_loop(asyncio.new_event_loop())
		asyncio.get_event_loop().run_until_complete(websockets.serve(self.listener, Config.get("WEBSOCKET", "LISTEN_ADDR"), Config.get("WEBSOCKET", "LISTEN_PORT")))
		asyncio.get_event_loop().run_until_complete(self.responder())
		asyncio.get_event_loop().run_forever()

	#----------------------------------------------------------------------
	async def listener(self, ws, path):
		await self.register(ws)
		try:
			async for msg in ws:
				await Queue.asAdd("RECV", json.loads(msg))
		finally:
			await self.unregister(ws)

	#----------------------------------------------------------------------
	async def register(self, websocket):
		self.sockets.add(websocket)

	#----------------------------------------------------------------------
	async def responder(self):
		while True:
			msg = await Queue.asGet("SEND")
			#if "PLAYER" in msg.keys():
			#	if "TIMER" not in msg["PLAYER"].keys():
			#		print("Response: {}".format(msg))

			for ws in self.sockets:
				await ws.send(json.dumps(msg))

	#----------------------------------------------------------------------
	async def unregister(self, websocket):
		self.sockets.remove(websocket)
