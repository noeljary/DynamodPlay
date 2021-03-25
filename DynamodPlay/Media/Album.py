from Media.MediaGroup import MediaGroup

########################################################################
class Album(MediaGroup):

	#----------------------------------------------------------------------
	def __init__(self, id, name, sort, artist, img, year, updated):
		self.tracks = []

		self.setId(id)
		self.setName(name)
		self.setSort(sort)
		self.setArtistName(artist)
		self.setImg(img)
		self.setYear(year)
		self.setUpdated(updated)

	#----------------------------------------------------------------------
	def getArtistName(self):
		return self.artist

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
	def getYear(self):
		return self.year

	#----------------------------------------------------------------------
	def setArtistName(self, artist):
		self.artist = artist

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
	def setYear(self, year):
		self.year = year

	#----------------------------------------------------------------------
	def toDict(self):
		return {"ID": self.getId(), "NAME": self.getName(), "IMG": self.getImg(), "SORT": self.getSort(), "ARTIST": self.getArtistName(), "YEAR": self.getYear(), "UPDATED": None if not self.getUpdated() else self.getUpdated().strftime("%Y-%m-%d, %H:%M:%S")}
	
