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
		if not self.getAlbum(album.getId()):
			self.albums.append(album)
	
	#----------------------------------------------------------------------
	def addTrack(self, track):
		if not self.getTrack(track.getId()):
			self.tracks.append(track)

	#----------------------------------------------------------------------
	def getAlbum(self, id):
		for album in self.albums:
			if album.getId() == id:
				return album

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
	def getTrack(self, id):
		for track in self.tracks:
			if track.getId() == id:
				return track

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
	
