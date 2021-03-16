from Config import Config

########################################################################
class LocalRadioAdapterStation:

	#----------------------------------------------------------------------
	def __init__(self, station):
		self.id     = station["KEY"]
		self.name   = station["NAME"]
		self.img    = self.imgPath(self.id, station["IMG"])
		self.stream = station["STREAM"]

	#----------------------------------------------------------------------
	def imgPath(self, id, img):
		return "{}/{}.{}".format(Config.get("RADIO", "IMG_PATH"), id, img)

	#----------------------------------------------------------------------
	def toObj(self):
		return (self.id, self.name, self.img, self.stream)
