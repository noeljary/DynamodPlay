from Config import Config

########################################################################
class LocalRadioAdapterStation:

	#----------------------------------------------------------------------
	def __init__(self, station):
		self.id            = station["KEY"]
		self.name          = station["NAME"]
		self.img           = self.imgPath(self.id, station["IMG"])
		self.stream        = station["STREAM"]
		self.metadata_type = None if "METADATA" not in station.keys() else station["METADATA"]["TYPE"]
		self.metadata_conf = None

		# Collect Metadata Details If Set
		if self.metadata_type:
			self.metadata_conf = station["METADATA"][self.metadata_type]

	#----------------------------------------------------------------------
	def imgPath(self, id, img):
		return "{}/{}.{}".format(Config.get("RADIO", "IMG_PATH"), id, img)

	#----------------------------------------------------------------------
	def toObj(self):
		return (self.id, self.name, self.img, self.stream, self.metadata_type, self.metadata_conf)
