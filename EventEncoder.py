import json

class EventEncoder(json.JSONEncoder):
	def default(self, o):
		return o.__dict__
