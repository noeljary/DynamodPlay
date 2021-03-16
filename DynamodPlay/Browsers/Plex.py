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

			cls.content   = {"LIBRARIES": {}, "ARTISTS": {}, "ALBUMS": {}, "TRACKS": {}}

		return cls._instance

	#----------------------------------------------------------------------
	def getAlbums(self, library):
		keys = library.keys()
		if "ARTIST" in keys and "LIBRARY" in keys:
			return self.getAlbumsByArtist(library["LIBRARY"], library["ARTIST"])
		elif "LIBRARY" in keys:
			return self.getAlbumsByLibrary(library["LIBRARY"])

	#----------------------------------------------------------------------
	def getAlbumsByArtist(self, library, artist):
		if not self.content["ARTISTS"][artist].getAlbums():
			self.loadAlbumsByArtist(library, artist)

		albums = []
		for album in self.content["ARTISTS"][artist].getAlbums():
			albums.append(self.content["ALBUMS"][album].toDict())

		return {"LIBRARY": library, "ARTIST": artist, "ALBUMS": albums}

	#----------------------------------------------------------------------
	def getAlbumsByLibrary(self, library):
		if not self.content["LIBRARIES"][library].getAlbums():
			self.loadAlbumsByLibrary(library)
		
		albums = []
		for album in self.content["LIBRARIES"][library].getAlbums():
			albums.append(self.content["ALBUMS"][album].toDict())

		return {"LIBRARY": library, "ALBUMS": albums}

	#----------------------------------------------------------------------
	def getArtists(self, library):
		if "LIBRARY" not in library.keys():
			return

		if not self.content["LIBRARIES"][library["LIBRARY"]].getArtists():
			self.loadArtists(library["LIBRARY"])
		
		artists = []
		for artist in self.content["LIBRARIES"][library["LIBRARY"]].getArtists():
			artists.append(self.content["ARTISTS"][artist].toDict())

		return {"LIBRARY": library["LIBRARY"], "ARTISTS": artists}

	#----------------------------------------------------------------------
	def getKey(self):
		return self.key

	#----------------------------------------------------------------------
	def getLibraries(self):
		if not self.content["LIBRARIES"]:
			self.loadLibraries()

		libraries = []
		for library in self.content["LIBRARIES"].keys():
			libraries.append(self.content["LIBRARIES"][library].toDict())

		return {"LIBRARIES": libraries}

	#----------------------------------------------------------------------
	def getTracks(self, hierarchy):
		keys = hierarchy.keys()
		if "ALBUM" in keys and "LIBRARY" in keys:
			return self.getTracksByAlbum(hierarchy["LIBRARY"], hierarchy["ALBUM"])
		elif "ARTIST" in keys and "LIBRARY" in keys:
			return self.getTracksByArtist(hierarchy["LIBRARY"], hierarchy["ARTIST"])
		elif "LIBRARY" in keys:
			return self.getTracksByLibrary(hierarchy["LIBRARY"])

	#----------------------------------------------------------------------
	def getTracksByAlbum(self, library, album):
		if not self.content["ALBUMS"][album].getTracks():
			self.loadTracksByAlbum(library, album)

		tracks = []
		for track in self.content["ALBUMS"][album].getTracks():
			tracks.append(self.content["TRACKS"][track].toDict())

		return {"LIBRARY": library, "ALBUM": album, "TRACKS": tracks}

	#----------------------------------------------------------------------
	def getTracksByArtist(self, library, artist):
		if not self.content["ARTISTS"][artist].getTracks():
			self.loadTracksByArtist(library, artist)

		tracks = []
		for track in self.content["ARTISTS"][artist].getTracks():
			tracks.append(self.content["TRACKS"][track].toDict())

		return {"LIBRARY": library, "ARTIST": artist, "TRACKS": tracks}

	#----------------------------------------------------------------------
	def getTracksByLibrary(self, library):
		if not self.content["LIBRARIES"][library].getTracks():
			self.loadTracksByLibrary(library)

		tracks = []
		for track in self.content["LIBRARIES"][library].getTracks():
			tracks.append(self.content["TRACKS"][track].toDict())

		return {"LIBRARY": library, "TRACKS": tracks}

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
	def loadArtists(self, library):
		for artist in self.plex.library.sectionByID(library).all():
			new_artist = Artist(*PlexAdapterArtist(artist).toObj())
			self.content["LIBRARIES"][library].addArtist(new_artist.getId())
			if new_artist.getId() not in self.content["ARTISTS"].keys():
				self.content["ARTISTS"][new_artist.getId()] = new_artist

	#----------------------------------------------------------------------
	def loadAlbumsByArtist(self, library, artist):
		for album in self.plex.library.sectionByID(library).fetchItem(artist).albums():
			new_album = Album(*PlexAdapterAlbum(album).toObj())
			self.content["ARTISTS"][artist].addAlbum(new_album.getId())
			if new_album.getId() not in self.content["ALBUMS"].keys():
				self.content["ALBUMS"][new_album.getId()] = new_album

	#----------------------------------------------------------------------
	def loadAlbumsByLibrary(self, library):
		for album in self.plex.library.sectionByID(library).albums():
			new_album = Album(*PlexAdapterAlbum(album).toObj())
			self.content["LIBRARIES"][library].addAlbum(new_album.getId())
			if new_album.getId() not in self.content["ALBUMS"].keys():
				self.content["ALBUMS"][new_album.getId()] = new_album

	#----------------------------------------------------------------------
	def loadLibraries(self):
		for library in self.plex.library.sections():
			if library.CONTENT_TYPE == Config.get("PLEX", "LIB_TYPE"):
				new_library = Library(*PlexAdapterLibrary(library).toObj())
				if new_library.getId() not in self.content["LIBRARIES"].keys():
					self.content["LIBRARIES"][new_library.getId()] = new_library

	#----------------------------------------------------------------------
	def loadTracksByAlbum(self, library, album):
		for track in self.plex.library.sectionByID(library).fetchItem(album).tracks():
			new_track = Track(*PlexAdapterTrack(track).toObj())
			self.content["ALBUMS"][album].addTrack(new_track.getId())
			if new_track.getId() not in self.content["TRACKS"].keys():
				self.content["TRACKS"][new_track.getId()] = new_track

	#----------------------------------------------------------------------
	def loadTracksByArtist(self, library, artist):
		for track in self.plex.library.sectionByID(library).fetchItem(artist).tracks():
			new_track = Track(*PlexAdapterTrack(track).toObj())
			self.content["ARTISTS"][artist].addTrack(new_track.getId())
			if new_track.getId() not in self.content["TRACKS"].keys():
				self.content["TRACKS"][new_track.getId()] = new_track

	#----------------------------------------------------------------------
	def loadTracksByLibrary(self, library):
		for track in self.plex.library.sectionByID(library).searchTracks():
			new_track = Track(*PlexAdapterTrack(track).toObj())
			self.content["LIBRARIES"][library].addTrack(new_track.getId())
			if new_track.getId() not in self.content["TRACKS"].keys():
				self.content["TRACKS"][new_track.getId()] = new_track

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
