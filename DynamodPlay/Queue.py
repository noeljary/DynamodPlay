import asyncio
import collections
import time

########################################################################
class Queue:

	queues = {}

	#---------------------------------------------------------------------------
	def init():
		Queue.queues["RECV"]  = collections.deque()
		Queue.queues["SEND"]  = collections.deque()

	#---------------------------------------------------------------------------
	async def asAdd(queue, value):
		Queue.queues[queue].append(value)

	#---------------------------------------------------------------------------
	async def asGet(queue):
		while True:
			try:
				msg = Queue.queues[queue].popleft()
				return msg
			except IndexError:
				await asyncio.sleep(0.001)

	#---------------------------------------------------------------------------
	def add(queue, value):
		Queue.queues[queue].append(value)

	#---------------------------------------------------------------------------
	def get(queue):
		while True:
			try:
				return Queue.queues[queue].popleft()
			except IndexError:
				time.sleep(0.001)