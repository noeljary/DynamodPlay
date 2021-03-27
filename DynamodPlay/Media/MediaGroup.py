import random

########################################################################
class MediaGroup:

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
	def getTrackNext(self, track):
		idx = self.tracks.index(track)
		if idx + 1 < len(self.tracks):
			return self.tracks[idx + 1]
		else:
			return None

	#----------------------------------------------------------------------
	def getTrackPrev(self, track):
		idx = self.tracks.index(track)
		if idx > 0:
			return self.tracks[idx - 1]
		else:
			return None

	#----------------------------------------------------------------------
	def getTrackRnd(self):
		return self.tracks[random.randint(0, self.getNumTracks() - 1)]

	#----------------------------------------------------------------------
	def getTracks(self):
		return self.tracks
