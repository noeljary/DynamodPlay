from Config import Config

########################################################################
class PlexAdapterLibrary:

	#----------------------------------------------------------------------
	def __init__(self, library):
		self.id     = library.key
		self.name   = library.title
		self.updated = library.updatedAt

	#----------------------------------------------------------------------
	def toObj(self):
		return (self.id, self.name, self.updated)

########################################################################
class PlexAdapterArtist:

	#----------------------------------------------------------------------
	def __init__(self, artist):
		self.id      = artist.ratingKey
		self.name    = artist.title
		self.sort    = artist.titleSort
		self.img     = str(PlexAdapterImg(artist.thumb))
		self.updated = artist.updatedAt

	#----------------------------------------------------------------------
	def toObj(self):
		return (self.id, self.name, self.sort, self.img, self.updated)

########################################################################
class PlexAdapterAlbum:

	#----------------------------------------------------------------------
	def __init__(self, album):
		self.id      = album.ratingKey
		self.name    = album.title
		self.sort    = album.titleSort
		self.artist  = album.artist().title
		self.img     = str(PlexAdapterImg(album.thumb if album.thumb else album.parentThumb))
		self.year    = album.year
		self.updated = album.updatedAt

	#----------------------------------------------------------------------
	def toObj(self):
		return (self.id, self.name, self.sort, self.artist, self.img, self.year, self.updated)

########################################################################
class PlexAdapterTrack:

	#----------------------------------------------------------------------
	def __init__(self, track):
		self.id       = track.ratingKey
		self.name     = track.title
		self.sort     = track.titleSort
		self.duration = track.duration
		self.stream   = track.getStreamURL()
		self.setImg(track)

	#----------------------------------------------------------------------
	def setImg(self, track):
		try:
			self.img = str(PlexAdapterImg(track.thumb))
		except AttributeError:
			try:
				self.img = str(PlexAdapterImg(track.parentThumb))
			except AttributeError:
				try:
					self.img = str(PlexAdapterImg(track.grandparentThumb))
				except AttributeError:
					self.img = None

	#----------------------------------------------------------------------
	def toObj(self):
		return (self.id, self.name, self.sort, self.duration, self.img, self.stream)

########################################################################
class PlexAdapterImg:

	#----------------------------------------------------------------------
	def __init__(self, img):
		url   = Config.get("PLEX", "ADDR")
		token = Config.get("PLEX", "TOKEN")
		self.url = "{}{}?X-Plex-Token={}".format(url, img, token)

	#----------------------------------------------------------------------
	def __str__(self):
		return self.url