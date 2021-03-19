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
		if not self.getAlbum(album.getId()):
			self.albums.append(album)

	#----------------------------------------------------------------------
	def addArtist(self, artist):
		if not self.getArtist(artist.getId()):
			self.artists.append(artist)

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
	def getArtist(self, id):
		for artist in self.artists:
			if artist.getId() == id:
				return artist

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
	def getTrack(self, id):
		for track in self.tracks:
			if track.getId() == id:
				return track

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
