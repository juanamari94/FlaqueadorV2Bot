from BotErrors.RepeatedUserError import RepeatedUserError
from BotErrors.NonExistentUserError import NonExistentUserError

class Event:

	def __init__(self, name, user, chat_id, subscribers=[]):
		self.title = name
		self.admin = user
		self.chat_id = chat_id
		self.subscribers = subscribers

	def add_subscriber(self, subscriber):
		if self._exists(subscriber):
			raise RepeatedUserError('User already exists.')
		else:
			self.subscribers.append(subscriber)

	def remove_subscriber(self, subscriber):
		if self._exists(subscriber):
			self.subscribers.remove(subscriber)
		else:
			raise NonExistentUserError('User does not exist.')

	def _exists(self, subscriber):
		user_ids = []
		for user in self.subscribers:
			user_ids.append(user.user_id)
		if subscriber.user_id in user_ids:
			return True
		return False
