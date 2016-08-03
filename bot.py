#!/usr/bin/python3.5
# -*- coding: utf-8 -*-
import telebot
import cherrypy
import config
import utils
import subprocess
import os
import logging
from sys import path
from random import shuffle
import webhook

bot = telebot.TeleBot(config.token)

logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)

markup = utils.generate_markup();

class WebhookServer(object):
	@cherrypy.expose
	def index(self):
		if 'content-length' in cherrypy.request.headers and \
					'content-type' in cherrypy.request.headers and \
					cherrypy.request.headers['content-type'] == 'application/json':
			length = int(cherrypy.request.headers['content-length'])
			json_string = cherrypy.request.body.read(length).decode("utf-8")
			update = telebot.types.Update.de_json(json_string)
			bot.process_new_updates([update])
			return 'hi'
		else:
			raise cherrypy.HTTPError(403)

bot.remove_webhook()

bot.set_webhook(url=webhook.WEBHOOK_URL_BASE + webhook.WEBHOOK_URL_PATH, certificate=open(webhook.WEBHOOK_SSL_CERT, 'r'))

if config.send_start_message:
	bot.send_message(config.bot_admin_id, "mimibot is started", parse_mode="HTML", reply_markup=markup)
	bot.send_message(88783259, "mimibot is started", parse_mode="HTML", reply_markup=markup)

@bot.message_handler(commands=['start'])
def start(message):
	bot.send_message(config.bot_admin_id, "new id: " + str(message.chat.id) + "\n" + str(message.chat.username) + "\r\n" + str(message.chat.first_name) + " " + str(message.chat.last_name), reply_markup=markup)

@bot.message_handler(commands=['help'])
def start(message):
	if utils.check_users(message.chat.id):
		bot.send_message(message.chat.id, "/status\n/thanks\n/conn\n/ss\n", reply_markup=markup)

@bot.message_handler(commands=['conn'])
def status(message):
	if utils.check_users(message.chat.id):
		bot.send_message(message.chat.id, "ssh odroid@"+config.host + " -p " + str(config.outport), reply_markup=markup)
	
@bot.message_handler(commands=['status'])
def status(message):
	if utils.check_users(message.chat.id):
		response = utils.parse_status()
		if response['status'] == "graph":
			try:
				photo = open(response['filename'], 'rb')
				bot.send_photo(message.chat.id, photo)
				try:
					os.remove(response['filename'])
				except Exception as e:
					bot.send_message(message.chat.id, "can't delete graph file", reply_markup=markup)
			except Exception as e:
				bot.send_message(message.chat.id, "can't open graph file", reply_markup=markup)
		elif response['status'] == "text":
			text = ''
			for line in response['text']:
				text += str(line) + "\n"
			bot.send_message(message.chat.id, text, reply_markup=markup)
		else:
			bot.send_message(message.chat.id, response['text'], reply_markup=markup)
	
@bot.message_handler(commands=['thanks'])
def thanks(message):
	if utils.check_users(message.chat.id):
		markup = utils.generate_markup()
		bot.send_sticker(message.chat.id, utils.get_random_sticker(), reply_markup=markup)

@bot.message_handler(commands=['ss'])
def start_sms_service(message):
	if utils.check_users(message.chat.id):
		utils.start_sms_service()
		bot.send_sticker(message.chat.id, utils.get_random_sticker_cool(), reply_markup=markup)

@bot.message_handler(content_types=['sticker'])
def handle_stickers(message):
	if utils.check_users(message.chat.id):
		bot.send_message(message.chat.id, '"' + message.sticker.file_id + '", ', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def test_callback(call):
	mid = call.from_user.id
	data = call.data
	if utils.check_users(mid):
		if data == "ss restart":
			utils.start_sms_service()
			bot.send_sticker(mid, utils.get_random_sticker_cool(), reply_markup=markup)
		elif data == "thanks":
			markup = utils.generate_markup()
			bot.send_sticker(mid, utils.get_random_sticker(), reply_markup=markup)
		elif data == "conn":
			markup = utils.generate_markup()
			bot.send_message(mid, "ssh odroid@"+config.host + " -p " + str(config.outport), reply_markup=markup)
		elif data == "status":
			response = utils.parse_status()
			if response['status'] == "graph":
				try:
					photo = open(response['filename'], 'rb')
					bot.send_photo(mid, photo)
					try:
						os.remove(response['filename'])
					except Exception as e:
						bot.send_message(mid, "can't delete graph file", reply_markup=markup)
				except Exception as e:
					bot.send_message(mid, "can't open graph file", reply_markup=markup)
			elif response['status'] == "text":
				text = ''
				for line in response['text']:
					text += str(line) + "\n"
				bot.send_message(mid, text, reply_markup=markup)
			else:
				bot.send_message(mid, response['text'], reply_markup=markup)
		else:
			bot.send_sticker(mid, "BQADAgAD5gADDBrwAiHi-1ZEBxPNAg", reply_markup=markup)

cherrypy.config.update({
	'server.socket_host': webhook.WEBHOOK_LISTEN,
	'server.socket_port': webhook.WEBHOOK_PORT,
	'server.ssl_module': 'builtin',
	'server.ssl_certificate': webhook.WEBHOOK_SSL_CERT,
	'server.ssl_private_key': webhook.WEBHOOK_SSL_PRIV
})

cherrypy.quickstart(WebhookServer(), webhook.WEBHOOK_URL_PATH, {'/': {}})
