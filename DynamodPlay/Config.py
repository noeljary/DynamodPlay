import configparser
import sys

########################################################################
class Config:

	config = None

	#----------------------------------------------------------------------
	def init():
		# Check config provided
		if len(sys.argv) > 1:
			# Parse config file from start args
			Config.config = configparser.ConfigParser()
			Config.config.read(sys.argv[1])
		else:
			# Exit without configs provided
			print("COULD NOT START - NO CONFIG FILE")
			exit(-1)


	#----------------------------------------------------------------------
	def get(category, name, default = None):
		# Return config value
		if category not in Config.config.keys():
			return default
		if name not in Config.config[category].keys():
			return default

		return Config.config[category][name]
