#!/usr/bin/python3.5
# -*- coding: utf-8 -*-
import telebot
import config

bot = telebot.TeleBot(config.token)

bot.send_message(config.bot_admin_id, "mimibot is started", parse_mode="HTML", reply_markup=markup)
