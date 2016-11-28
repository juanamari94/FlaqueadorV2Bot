#!/usr/bin/env python
# -*- coding: utf-8 -*-

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from pymongo import MongoClient
from Event import Event
from User import User
import logging
import constants
import json
from BotErrors.RepeatedUserError import RepeatedUserError
from EventEncoder import EventEncoder

updater = Updater(constants.BOT_API_KEY)
dispatcher = updater.dispatcher
handlers = []
client = MongoClient(constants.MONGODB_URI)
db = client.graciasporvenirbotdb

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def start(bot, update):
	bot.sendMessage(chat_id=update.message.chat_id, text="Hi!")


def error(bot, update, error):
	logger.warn('Update "%s" caused error "%s"' % (update, error))

def parse_user(update):
	user_info = update.message.from_user
	user_id = user_info.id
	user_name = user_info.first_name + ' ' + user_info.last_name
	return User(user_id, user_name)


def parse_command(update):
	event_string = str(update.message['text']).split(" ", 1)
	return event_string[1]


def create_event(bot, update):
	chat_id = update.message.chat_id
	user = parse_user(update)
	event_title = parse_command(update)
	event = Event(event_title, user, chat_id)
	event.add_subscriber(user)
	event.add_subscriber(User(1, "pepito"))
	db.events.insert(json.loads(to_json(event)))
	bot.sendMessage(chat_id=chat_id, text='Evento: ' + event.title + ' creado!')


def to_json(event):
	return json.dumps(event, cls=EventEncoder)


def parse_event_to_query(event):
	return json.loads(to_json(event))


def join_event(bot, update):
	chat_id = update.message.chat_id
	user = parse_user(update)
	event_name = parse_command(update)
	event_query = db.events.find_one({'title': event_name})
	document_id = event_query['_id']
	event = parse_event_dict(event_query)
	result = try_adding_subscriber(event, user)
	if result is not True:
		bot.sendMessage(chat_id=chat_id, text='Ya estás suscrito a ese evento.')
	else:
		query = parse_event_to_query(event)
		db.events.update({'_id': document_id}, query, True)
		bot.sendMessage(chat_id=chat_id, text=user.name + " te has unido al evento!")


def try_adding_subscriber(event, user):
	try:
		event.add_subscriber(user)
		return True
	except RepeatedUserError:
		return False


def get_event(update):
	event_title = parse_command(update)
	return db.events.find_one({'title': event_title})


def parse_user_dict(user_dict):
	user_id = user_dict['user_id']
	user_name = user_dict['name']
	return User(user_id, user_name)


def parse_event_dict(event):
	event_title = event['title']
	admin_user = parse_user_dict(event['admin'])
	chat_id = event['chat_id']
	subscribers = []
	for k in event['subscribers']:
		user = parse_user_dict(k)
		subscribers.append(user)
	return Event(event_title, admin_user, chat_id, subscribers)


def add_handlers():
	handlers.append(CommandHandler("start", start))
	handlers.append(MessageHandler(Filters.text, handle_text))
	handlers.append(CommandHandler("create_event", create_event))
	handlers.append(CommandHandler("join_event", join_event))


def handle_text(bot, update):
	from TextHandler import TextHandler
	message_body = update.message['text'].lower()
	print update.message
	text_handler = TextHandler()
	text_handler.load_defaults()
	handler_keys = text_handler.text_message_map.keys()
	"""for key in handler_keys:
	if key in message_body:
		bot.sendMessage(chat_id=update.message.chat_id, text=text_handler.get_handler(key))"""


def start_handlers():
	for handler in handlers:
		dispatcher.add_handler(handler)
	dispatcher.add_error_handler(error)


def main():
	add_handlers()
	start_handlers()
	updater.start_polling()
	updater.idle()


if __name__ == '__main__':
	main()
