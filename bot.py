#!/usr/bin/env python
# -*- coding: utf-8 -*-

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import constants
import logging

updater = Updater(constants.BOT_API_KEY)
dispatcher = updater.dispatcher
handlers = []

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def start(bot, update):
	bot.sendMessage(chat_id=update.message.chat_id, text="Flaco")


def error(bot, update, error):
	logger.warn('Update "%s" caused error "%s"' % (update, error))


def add_handlers():
	handlers.append(CommandHandler("start", start))
	handlers.append(MessageHandler(Filters.text, handle_text))


def handle_text(bot, update):
	from TextHandler import TextHandler
	message_body = update.message['text'].lower()
	print update.message
	text_handler = TextHandler()
	text_handler.load_defaults()
	handler_keys = text_handler.text_message_map.keys()
	for key in handler_keys:
		if key in message_body:
			bot.sendMessage(chat_id=update.message.chat_id, text=text_handler.get_handler(key))


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
