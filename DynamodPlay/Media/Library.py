from Media.MediaGroup import MediaGroup

########################################################################
class Library(MediaGroup):

	#----------------------------------------------------------------------
	def __init__(self, id, name, updated):
		self.artists = []
		self.albums  = []
		self.tracks  = []

		self.setId(id)
		self.setName(name)
		self.setUpdated(updated)

	#----------------------------------------------------------------------
	def getId(self):
		return self.l_id

	#----------------------------------------------------------------------
	def getName(self):
		return self.name

	#----------------------------------------------------------------------
	def getUpdated(self):
		return self.updated

	#----------------------------------------------------------------------
	def setId(self, id):
		self.l_id = id

	#----------------------------------------------------------------------
	def setName(self, name):
		self.name = name

	#----------------------------------------------------------------------
	def setUpdated(self, updated):
		self.updated = updated

	#----------------------------------------------------------------------
	def toDict(self):
		return {"ID": self.getId(), "NAME": self.getName(), "UPDATED": None if not self.getUpdated() else self.getUpdated().strftime("%Y-%m-%d, %H:%M:%S")}
