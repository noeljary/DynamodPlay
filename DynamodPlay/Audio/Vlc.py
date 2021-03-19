import vlc

from Audio.AudioInterface import AudioInterface

########################################################################
class Vlc(AudioInterface):

	key = "VLC"

	#---------------------------------------------------------------------------
	def __init__(self, stream):
		self.vlc        = vlc.Instance()
		self.media_list = self.vlc.media_list_new([stream])
		self.player     = self.vlc.media_list_player_new()
		self.player.set_media_list(self.media_list)

	#----------------------------------------------------------------------
	def getKey():
		return Vlc.key

	#----------------------------------------------------------------------
	def getStatus(self):
		return self.isPlaying()

	#----------------------------------------------------------------------
	def isPlaying(self):
		return self.player.is_playing()

	#----------------------------------------------------------------------
	def play(self):
		self.player.play()
		return self.isPlaying()

	#----------------------------------------------------------------------
	def pause(self):
		self.player.pause()
		return self.isPlaying()

	#----------------------------------------------------------------------
	def stop(self):
		self.player.stop()
		return self.isPlaying()
