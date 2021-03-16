########################################################################
class Library:

	#----------------------------------------------------------------------
	def __init__(self, id, name, updated):
		self.artists = []
		self.albums  = []
		self.tracks  = []

		self.setId(id)
		self.setName(name)
		self.setUpdated(updated)

	#----------------------------------------------------------------------
	def addAlbum(self, album):
		if not album in self.albums:
			self.albums.append(album)

	#----------------------------------------------------------------------
	def addArtist(self, artist):
		if not artist in self.artists:
			self.artists.append(artist)

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
	def getArtist(self, artist):
		return self.artists[artist] if artist in self.artists.keys() else None

	#----------------------------------------------------------------------
	def getArtists(self):
		return self.artists

	#----------------------------------------------------------------------
	def getId(self):
		return self.l_id

	#----------------------------------------------------------------------
	def getName(self):
		return self.name

	#----------------------------------------------------------------------
	def getNumAlbums(self):
		return len(self.albums)

	#----------------------------------------------------------------------
	def getNumArtists(self):
		return len(self.artists)

	#----------------------------------------------------------------------
	def getNumTracks(self):
		return len(self.tracks)

	#----------------------------------------------------------------------
	def getTrack(self, track):
		return self.track[track] if track in self.tracks.keys() else None

	#----------------------------------------------------------------------
	def getTracks(self):
		return self.tracks

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
