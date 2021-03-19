from plexapi.server      import PlexServer

from Config              import Config
from Media.Library       import Library
from Media.Artist        import Artist
from Media.Album         import Album
from Media.Track         import Track
from Media.Adapters.Plex import *

########################################################################
class PlexBrowser:

	_instance = None

	key       = "PLEX"

	#----------------------------------------------------------------------
	def __new__(cls):
		if cls._instance is None:
			cls._instance = super(PlexBrowser, cls).__new__(cls)

			cls.libraries = []

		return cls._instance

	#----------------------------------------------------------------------
	def getAlbums(self, parents):
		if "ARTIST" in parents.keys():
			return self.getAlbumsByArtist(parents["LIBRARY"], parents["ARTIST"])
		else:
			return self.getAlbumsByLibrary(parents["LIBRARY"])

	#----------------------------------------------------------------------
	def getAlbumsByArtist(self, library, artist):
		if not self.getLibrary(library).getArtist(artist).getAlbums():
			self.loadAlbumsByArtist(self.getLibrary(library), self.getLibrary(library).getArtist(artist))

		albums = self.mediaObjToDict(self.getLibrary(library).getArtist(artist).getAlbums())

		return {"LIBRARY": library, "ARTIST": artist, "ALBUMS": albums}

	#----------------------------------------------------------------------
	def getAlbumsByLibrary(self, library):
		if not self.getLibrary(library).getAlbums():
			self.loadAlbumsByLibrary(self.getLibrary(library))

		albums = self.mediaObjToDict(self.getLibrary(library).getAlbums())

		return {"LIBRARY": library, "ALBUMS": albums}

	#----------------------------------------------------------------------
	def getArtists(self, parents):
		if not self.getLibrary(parents["LIBRARY"]).getArtists():
			self.loadArtists(self.getLibrary(parents["LIBRARY"]))

		artists = self.mediaObjToDict(self.getLibrary(parents["LIBRARY"]).getArtists())

		return {"LIBRARY": parents["LIBRARY"], "ARTISTS": artists}

	#----------------------------------------------------------------------
	def getKey(self):
		return self.key

	#----------------------------------------------------------------------
	def getLibraries(self):
		if not self.libraries:
			self.loadLibraries()

		libraries = self.mediaObjToDict(self.libraries)

		return {"LIBRARIES": libraries}

	#----------------------------------------------------------------------
	def getLibrary(self, library):
		for lib in self.libraries:
			if lib.getId() == library:
				return lib

	#----------------------------------------------------------------------
	def getTracks(self, parents):
		keys = parents.keys()
		if "ARTIST" in keys and "ALBUM" in keys:
			return self.getTracksByArtistAlbum(parents["LIBRARY"], parents["ARTIST"], parents["ALBUM"])
		elif "ALBUM" in keys:
			return self.getTracksByAlbum(parents["LIBRARY"], parents["ALBUM"])
		elif "ARTIST" in keys:
			return self.getTracksByArtist(parents["LIBRARY"], parents["ARTIST"])
		elif "LIBRARY" in keys:
			return self.getTracksByLibrary(parents["LIBRARY"])

	#----------------------------------------------------------------------
	def getTracksByAlbum(self, lib_id, al_id):
		library = self.getLibrary(lib_id)
		album   = library.getAlbum(al_id)
		if not album.getTracks():
			self.loadTracksByParent(library, album)

		tracks = self.mediaObjToDict(album.getTracks())

		return {"LIBRARY": lib_id, "ALBUM": al_id, "TRACKS": tracks}

	#----------------------------------------------------------------------
	def getTracksByArtist(self, lib_id, ar_id):
		library = self.getLibrary(lib_id)
		artist  = library.getArtist(ar_id)
		if not artist.getTracks():
			self.loadTracksByParent(library, artist)

		tracks = self.mediaObjToDict(artist.getTracks())

		return {"LIBRARY": lib_id, "ARTIST": ar_id, "TRACKS": tracks}

	#----------------------------------------------------------------------
	def getTracksByArtistAlbum(self, lib_id, ar_id, al_id):
		library = self.getLibrary(lib_id)
		artist  = library.getArtist(ar_id)
		album   = artist.getAlbum(al_id)
		if not album.getTracks():
			self.loadTracksByParent(library, album)

		tracks = self.mediaObjToDict(album.getTracks())

		return {"LIBRARY": lib_id, "ARTIST": ar_id, "ALBUM": al_id, "TRACKS": tracks}

	#----------------------------------------------------------------------
	def getTracksByLibrary(self, lib_id):
		library = self.getLibrary(lib_id)
		if not library.getTracks():
			self.loadTracksByLibrary(library)

		tracks = self.mediaObjToDict(library.getTracks())

		return {"LIBRARY": lib_id, "TRACKS": tracks}

	#----------------------------------------------------------------------
	def handleRequest(self, data):
		for key in data.keys():
			for mapping in self.request_map:
				if key == mapping["CODE"]:
					if mapping["ARGS"]:
						return mapping["FUNC"](data[key])
					else:
						return mapping["FUNC"]()

	#----------------------------------------------------------------------
	def loadAlbumsByArtist(self, library, artist):
		for album in self.plex.library.sectionByID(library.getId()).fetchItem(artist.getId()).albums():
			artist.addAlbum(Album(*PlexAdapterAlbum(album).toObj()))

	#----------------------------------------------------------------------
	def loadAlbumsByLibrary(self, library):
		for album in self.plex.library.sectionByID(library.getId()).albums():
			library.addAlbum(Album(*PlexAdapterAlbum(album).toObj()))

	#----------------------------------------------------------------------
	def loadArtists(self, library):
		for artist in self.plex.library.sectionByID(library.getId()).all():
			library.addArtist(Artist(*PlexAdapterArtist(artist).toObj()))

	#----------------------------------------------------------------------
	def loadLibraries(self):
		for library in self.plex.library.sections():
			if library.CONTENT_TYPE == Config.get("PLEX", "LIB_TYPE"):
				new_library = Library(*PlexAdapterLibrary(library).toObj())
				if not self.getLibrary(new_library.getId()):
					self.libraries.append(new_library)

	#----------------------------------------------------------------------
	def loadTracksByParent(self, library, parent):
		for track in self.plex.library.sectionByID(library.getId()).fetchItem(parent.getId()).tracks():
			parent.addTrack(Track(*PlexAdapterTrack(track).toObj()))

	#----------------------------------------------------------------------
	def loadTracksByLibrary(self, library):
		for track in self.plex.library.sectionByID(library.getId()).searchTracks():
			library.addTrack(Track(*PlexAdapterTrack(track).toObj()))

	#----------------------------------------------------------------------
	def mediaObjToDict(self, media):
		tmp_list = []
		for item in media:
			tmp_list.append(item.toDict())

		return tmp_list

	#----------------------------------------------------------------------
	def setHandlerMap(self):
		self.request_map = [
			{"CODE": "LIBRARIES", "FUNC": self.getLibraries, "ARGS": False},
			{"CODE": "ARTISTS",   "FUNC": self.getArtists,   "ARGS": True},
			{"CODE": "ALBUMS",    "FUNC": self.getAlbums,    "ARGS": True},
			{"CODE": "TRACKS",    "FUNC": self.getTracks,    "ARGS": True}
		]

	#----------------------------------------------------------------------
	def setup(self):
		self.url   = Config.get("PLEX", "ADDR")
		self.token = Config.get("PLEX", "TOKEN")
		self.plex  = PlexServer(self.url, self.token)
		self.setHandlerMap()
