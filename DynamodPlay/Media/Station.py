########################################################################
class Station:

	#----------------------------------------------------------------------
	def __init__(self, id, name, img, stream):
		self.setId(id)
		self.setName(name)
		self.setImg(img)
		self.setStream(stream)

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
	def getStream(self):
		return self.stream

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
	def setStream(self, stream):
		self.stream = stream

	#----------------------------------------------------------------------
	def toDict(self):
		return {"ID": self.getId(), "NAME": self.getName(), "IMG": self.getImg()}