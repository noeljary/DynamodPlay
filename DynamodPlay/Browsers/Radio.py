import json

from Config                    import Config
from Media.Station             import Station
from Media.Adapters.LocalRadio import *

########################################################################
class RadioBrowser:

	_instance = None

	key       = "LOCAL"

	#----------------------------------------------------------------------
	def __new__(cls):
		if cls._instance is None:
			cls._instance = super(RadioBrowser, cls).__new__(cls)

		return cls._instance

	#----------------------------------------------------------------------
	def getKey(self):
		return self.key

	#----------------------------------------------------------------------
	def getStations(self):
		if not self.station_list:
			self.loadStations()

		stations = []
		for station in self.station_list:
			stations.append(self.station_list[station].toDict())

		return {"STATIONS": stations}

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
	def loadStations(self):
		with open(Config.get("RADIO", "STATION_LIST")) as stations:
			station_list = json.load(stations)

		for station in station_list:
			new_station = Station(*LocalRadioAdapterStation(station).toObj())
			if new_station not in self.station_list:
				self.station_list[new_station.getId()] = new_station

	#----------------------------------------------------------------------
	def setHandlerMap(self):
		self.request_map = [
			{"CODE": "STATIONS", "FUNC": self.getStations, "ARGS": False},
		]

	#----------------------------------------------------------------------
	def setup(self):
		self.station_list = {}
		self.setHandlerMap()
