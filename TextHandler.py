from BotErrors import RepeatedKeywordError, NonExistentKeywordError
from TextHandlerSetupStrings import phrases_map

class TextHandler:
	def __init__(self):
		self.text_message_map = {}

	def add_keyword(self, keyword, message):
		if keyword not in self.text_message_map:
			self.text_message_map[keyword] = message
		else:
			raise RepeatedKeywordError("This keyword " + repr(keyword) + " already exists.")

	def remove_keyword(self, keyword):
		if keyword in self.text_message_map:
			del (self.text_message_map[keyword])
		else:
			raise NonExistentKeywordError("This keyword " + keyword + " doesn't exist.")

	def get_handler(self, keyword):
		return self.text_message_map[keyword]

	# Load up default strings
	def load_defaults(self):
		for key, value in phrases_map.items():
			self.add_keyword(key, value)
