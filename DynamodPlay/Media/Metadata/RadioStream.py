import re
import requests

from io        import BytesIO
from threading import Thread

########################################################################
class RadioStream(Thread):

	key = "STREAM"

	#----------------------------------------------------------------------
	def __init__(self, station, update_client, is_playing):
		Thread.__init__(self)

		# Metadata Configuration
		self.url           = station.getStream()
		self.metadata_conf = station.getMetadataConf()

		# Links to Parent Player Functions
		self.updateClient = update_client
		self.isPlaying    = is_playing

		self.running      = True

		self.start()

	#----------------------------------------------------------------------
	def getKey():
		return RadioStream.key

	#----------------------------------------------------------------------
	def run(self):
		r = requests.get(self.url, headers={"Icy-MetaData": "1", "User-Agent": "VLC/3.0.12 LibVLC/3.0.12"}, stream=True)

		# Exit Thread if not Correct Implementation
		if not "icy-metaint" in r.headers.keys():
			return

		# Ensure Encoding is Set
		if r.encoding is None:
			r.encoding  = "utf-8"

		# Initialise Loop Vars
		data_is_meta    = False
		byte_counter    = 0
		meta_counter    = 0
		metadata_buffer = BytesIO()
		metadata_size   = int(r.headers["icy-metaint"]) + 255

		# Prepare REGEX Ahead of Loop
		re_meta         = re.compile(f"StreamTitle={self.metadata_conf['REGEX']}".encode("utf-8"))

		for byte in r.iter_content(1):
			# Build Received Data into Message 
			byte_counter += 1

			if (byte_counter <= 2048):
				pass

			if (byte_counter > 2048):
				if (meta_counter == 0):
					meta_counter += 1
				elif (meta_counter <= int(metadata_size + 1)):
					metadata_buffer.write(byte)
					meta_counter += 1
				else:
					data_is_meta = True

			if (byte_counter > 2048 + metadata_size):
				byte_counter = 0

			# Got Metadata from Stream
			if data_is_meta:
				metadata_buffer.seek(0)
				meta   = metadata_buffer.read().rstrip(b'\0')
				artist = None
				track  = None

				# Regex Match Packet for Metadata
				m = re_meta.search(bytes(meta))
				if m:
					# Artist/Host
					if self.metadata_conf["ARTIST_GRP"] >= 1:
						artist = m.group(self.metadata_conf["ARTIST_GRP"]).decode(r.encoding, errors='replace')

					# Track/Show
					if self.metadata_conf["TRACK_GRP"] >= 1:
						track = m.group(self.metadata_conf["TRACK_GRP"]).decode(r.encoding, errors='replace')

					self.updateClient(artist, track, r.headers["icy-name"], None)

                # Reset Loop Vars
				byte_counter    = 0
				meta_counter    = 0
				metadata_buffer = BytesIO()
				data_is_meta    = False

			# Break out of Thread when Player Stops
			if not self.running:
				return

	#----------------------------------------------------------------------
	def terminate(self):
		self.running = False