########################################################################
class Station:

	#----------------------------------------------------------------------
	def __init__(self, id, name, img, stream, metadata_type, metadata_conf):
		self.setId(id)
		self.setName(name)
		self.setImg(img)
		self.setStream(stream)
		self.setMetadata(metadata_type, metadata_conf)

	#----------------------------------------------------------------------
	def getId(self):
		return self.id

	#----------------------------------------------------------------------
	def getImg(self):
		return self.img

	#----------------------------------------------------------------------
	def getMetadataConf(self):
		return self.metadata_conf

	#----------------------------------------------------------------------
	def getMetadataType(self):
		return self.metadata_type

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
	def setMetadata(self, metadata_type, metadata_conf):
		self.metadata_type = metadata_type
		self.metadata_conf = metadata_conf

	#----------------------------------------------------------------------
	def setName(self, name):
		self.name = name

	#----------------------------------------------------------------------
	def setStream(self, stream):
		self.stream = stream

	#----------------------------------------------------------------------
	def toDict(self):
		return {"ID": self.getId(), "NAME": self.getName(), "IMG": self.getImg()}