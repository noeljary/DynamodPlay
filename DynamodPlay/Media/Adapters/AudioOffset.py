########################################################################
class AudioOffsets:

	#----------------------------------------------------------------------
	def plex(stream, offset):
		return stream.replace("offset=0", "offset={}".format(offset))
