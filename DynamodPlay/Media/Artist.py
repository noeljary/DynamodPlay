from Media.MediaGroup import MediaGroup

########################################################################
class Artist(MediaGroup):

	#----------------------------------------------------------------------
	def __init__(self, id, name, sort, img, updated):
		self.albums = []
		self.tracks = []

		self.setId(id)
		self.setName(name)
		self.setSort(sort)
		self.setImg(img)
		self.setUpdated(updated)

	#----------------------------------------------------------------------
	def getId(self):
		return self.a_id

	#----------------------------------------------------------------------
	def getImg(self):
		return self.img

	#----------------------------------------------------------------------
	def getName(self):
		return self.name

	#----------------------------------------------------------------------
	def getSort(self):
		return self.sort

	#----------------------------------------------------------------------
	def getUpdated(self):
		return self.updated

	#----------------------------------------------------------------------
	def setId(self, id):
		self.a_id = id

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
	def setUpdated(self, updated):
		self.updated = updated

	#----------------------------------------------------------------------
	def toDict(self):
		return {"ID": self.getId(), "NAME": self.getName(), "IMG": self.getImg(), "SORT": self.getSort(), "UPDATED": None if not self.getUpdated() else self.getUpdated().strftime("%Y-%m-%d, %H:%M:%S")}
	
