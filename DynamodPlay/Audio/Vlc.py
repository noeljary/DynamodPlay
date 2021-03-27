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
		self.playing    = False

	#----------------------------------------------------------------------
	def getKey():
		return Vlc.key

	#----------------------------------------------------------------------
	def getStatus(self):
		return self.isPlaying()

	#----------------------------------------------------------------------
	def isPlaying(self):
		return self.playing and self.player.is_playing()

	#----------------------------------------------------------------------
	def play(self):
		self.player.play()
		self.playing = True
		return self.isPlaying()

	#----------------------------------------------------------------------
	def pause(self):
		self.player.pause()
		self.playing = False
		return self.isPlaying()

	#----------------------------------------------------------------------
	def stop(self):
		self.player.stop()
		self.playing = False
		return self.isPlaying()
