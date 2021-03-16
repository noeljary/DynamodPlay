########################################################################
class Artist:

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
	def addAlbum(self, album):
		if not album in self.albums:
			self.albums.append(album)
	
	#----------------------------------------------------------------------
	def addTrack(self, track):
		if not track in self.tracks:
			self.tracks.append(track)

	#----------------------------------------------------------------------
	def getAlbum(self, album):
		return self.albums[album] if album in self.albums.keys() else None

	#----------------------------------------------------------------------
	def getAlbums(self):
		return self.albums

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
	def getNumAlbums(self):
		return len(self.albums)

	#----------------------------------------------------------------------
	def getNumTracks(self):
		return len(self.tracks)

	#----------------------------------------------------------------------
	def getSort(self):
		return self.sort

	#----------------------------------------------------------------------
	def getUpdated(self):
		return self.updated

	#----------------------------------------------------------------------
	def getTrack(self, track):
		return self.track[track] if track in self.tracks.keys() else None

	#----------------------------------------------------------------------
	def getTracks(self):
		return self.tracks

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
	
