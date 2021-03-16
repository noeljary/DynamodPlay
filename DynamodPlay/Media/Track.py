import datetime

########################################################################
class Track:

	#----------------------------------------------------------------------
	def __init__(self, id, name, sort, duration, img, stream):
		self.setId(id)
		self.setName(name)
		self.setSort(sort)
		self.setDuration(duration)
		self.setImg(img)
		self.setStream(stream)

	#----------------------------------------------------------------------
	def _convertTimestampToDuration(raw_duration):
		return datetime.datetime.fromtimestamp(raw_duration / 1000).strftime("%H:%M:%S" if raw_duration >= 3600000 else "%M:%S")

	#----------------------------------------------------------------------
	def getDuration(self):
		return self.duration

	#----------------------------------------------------------------------
	def getId(self):
		return self.id

	#----------------------------------------------------------------------
	def getImg(self):
		return self.img

	#----------------------------------------------------------------------
	def getName(self):
		return self.name

	#----------------------------------------------------------------------
	def getRawDuration(self):
		return self.raw_duration

	#----------------------------------------------------------------------
	def getSort(self):
		return self.sort

	#----------------------------------------------------------------------
	def getStream(self):
		return self.stream

	#----------------------------------------------------------------------
	def setDuration(self, duration):
		self.raw_duration = duration
		self.duration     = Track._convertTimestampToDuration(duration)

	#----------------------------------------------------------------------
	def setId(self, id):
		self.id = id

	#----------------------------------------------------------------------
	def setImg(self, img):
		self.img = img

	#----------------------------------------------------------------------
	def setName(self, name):
		self.name = name

	#----------------------------------------------------------------------
	def setSort(self, sort):
		self.sort = sort

	#----------------------------------------------------------------------
	def setStream(self, stream):
		self.stream = stream

	#----------------------------------------------------------------------
	def toDict(self):
		return {"ID": self.getId(), "NAME": self.getName(), "SORT": self.getSort(), "DURATION": self.getDuration(), "RAW_DURATION": self.getRawDuration(), "IMG": self.getImg()}
