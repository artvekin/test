# -*- coding: utf-8 -*-
import shelve
from datetime import datetime, date
import time
from telebot import types
from random import shuffle
import random
from PIL import Image, ImageDraw, ImageFont
import cl_modems
import subprocess
import os
import sys

def generate_markup():
	markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
	markup.row("/status", "/thanks", "/conn", "/ss")
	return markup
	
def generate_inline_keyboard():
	markup = types.InlineKeyboardMarkup()
	but = types.InlineKeyboardButton(text="статус модемов", callback_data="status")
	markup.row(but)
	but = types.InlineKeyboardButton(text="ребутнуть смс сервис", callback_data="ss restart")
	markup.row(but)
	but = types.InlineKeyboardButton(text="поблагодарить", callback_data="thanks")
	markup.row(but)
	but = types.InlineKeyboardButton(text="получить данные для подключения", callback_data="conn")
	markup.row(but)
	return markup
	
def get_random_sticker():
	stickers = [
		"BQADBAADygIAAlI5kwbYObFgvYTn-wI", 
		"BQADAgADJgADJFGiBDyqoGDHBrgsAg", 
		"BQADAwADlAEAAr-MkATnQsDAc_3XPgI", 
		"BQADAgADrwoAAkKvaQAB2wAB6Uqa272IAg", 
		"BQADAgAD_gQAAkKvaQABbdMfUUWsaZEC", 
		"BQADAgADZgADaRIAAoiqPxWim9VDAg", 
		"BQADBAADVQEAAnCr1QTnpNwCNH_EfAI", 
		"BQADBAAD9wMAAjJQbQAB1mGSCaL2t0cC", 
		"BQADAgADEgUAAkKvaQABEN8qeK9AvDQC", 
		"BQADAgADkQoAAkKvaQABYVULgyRfM18C", 
		"BQADAgADiQADMyw8AAFn1vTWK-wg0QI", 
		"BQADAgADUAADQba6BLEs2p_qBi9HAg", 
		"BQADBAADTgADh5eiAj57gLRRng-iAg", 
		"BQADAgADVgADQba6BNVWsVZ1DBvNAg", 
		"BQADBAADLwADeh4OAAHiKBZ7kTUl6wI", 
		"BQADAgADDAADkWgMAAH5f4Jt6nba4AI"
	];
	
	shuffle(stickers)
	
	return stickers[0]
	
def get_random_sticker_cool():
	stickers = [
		"BQADAgADZAADaRIAAnpMlHIIH9NvAg",
		"BQADBAAD2QcAAhXc8gJus6FvCNfFXAI",
		"BQADAgADgQoAAkKvaQABkOKzP99UvuQC",
		"BQADAgADLAAD3XLZBGJHyoFeNMdpAg",
		"BQADAwADmQEAAr-MkATA2MTa5iQqmwI",
		"BQADAgADPAADSEvvAXyd7uNfZR2nAg",
		"BQADAgADbAADaRIAApqaYmVNYzg2Ag",
		"BQADAgADZgADaRIAAoiqPxWim9VDAg"
	]
	
	shuffle(stickers)
	
	return stickers[0]
	
def get_today():
	return str(time.strftime('%d.%m.%Y %H:%M:%S'))
	
def message_with_date(messagetext):
	return str(get_today()) + ":\n" + messagetext
	
def get_curr_password():
	dt = datetime.timetuple(datetime.today())
	weekday = dt.tm_wday + 1
	monthday = dt.tm_mday
	month = dt.tm_mon
	
	if len(str(month)) == 1:
		nmonth = int(str(month) + "0") + int(weekday)
	else:
		nmonth = int(str(month)[1] + str(month)[0]) + int(weekday)
		
	if len(str(monthday)) == 1:
		nmonthday = int(str(monthday) + "0") + int(weekday)
	else:
		nmonthday = int(str(monthday)[1] + str(monthday)[0]) + int(weekday)
	
	return str(nmonthday) + str(nmonth)

def check_password(password):
	return password == get_curr_password()
	
def check_users(id):
	users = [
		49289740, #Artem Glebov
		327199, #Alexey Sokolov
		7496857, #Maxim Ivshin
		88783259 #Nikolay Krivosheev
	]
	
	return users.count(id) > 0
		
def parse_status():
	text = []
	line_height = 15
	try:
		modems_status = open('/var/log/smstools/smsd_stats/status', 'r')
		
		modems = []
		
		counter1 = 0
		modems_count = 0
		good_modems = 0
		marginal_modems = 0
		bad_modems = 0
		
		tt = []
		
		for modem_status in modems_status:
			tt.append(modem_status)
			tt.append(counter1)
			if counter1 == 0:
				counter1 += 1
				continue
			current_modem = modem_status.split(",")
			if len(current_modem) == 5:
				if current_modem[1] != "Unknown\n":
					bad_modems += 1
					modem = cl_modems.modem()
					modem.name = "Unknown"
					modem.status = "Baaaad"
					modem.dbm = -140
					modem.set_colors()
					modems.append(modem)
			else:
				status = current_modem[5].split(":")[1].split(" ")[3]
				modem = cl_modems.modem()
				modem.name = current_modem[0].split(":")[0]
				modem.dbm = current_modem[5].split(":")[1].split(" ")[1]
				modem.status = status
				modem.set_colors()
				modems.append(modem)
				if status == "(Good)\n" or status == "(Workable)\n" or status == "(Excellent)\n":
					good_modems += 1
				elif status == "(Marginal)\n":
					marginal_modems += 1
				else:
					bad_modems += 1
			modems_count += 1
		if modems_count == good_modems:
			text.append("Всего модемов " + str(modems_count) + ", вроде все чёткие")
		else:
			text.append("Всего модемов " + str(modems_count) + "\n")
			text.append("  Хороших: " + str(good_modems) + "\n")
			text.append("  Плохих:    " + str(bad_modems) + "\n")
			text.append("  Бомжей:  " + str(marginal_modems) + "\n")
			
		tt.append("ollo2")
			
		subprocess.call(["/var/mimibot/smsdstatus.sh"]);
		try:
			statusfile = open('/var/mimibot/smsdstatus.txt', 'r')
			i = 0
			for line in statusfile:
				firstline = line
				firstline = firstline.split(" ")
				break
			
			if (firstline[len(firstline)-1] == "smsd\n"):
				status = "Status of SMSD: smsd is running."
			else:
				status = "Status of SMSD: smsd is NOT running."
			text.append(status)
			statusfile.close()
		except Exception as e:
			text.append(str(e))
		
		modems_dict = {
			'modems': modems, 
			'modems_count': modems_count, 
			'good_modems': good_modems, 
			'marginal_modems': marginal_modems, 
			'bad_modems': bad_modems,
			'response_text': text,
			'offset_size': len(text) * line_height,
			'filename': "/var/mimibot/images" + get_random_filename(20) + ".png",
			'main_text_color': '#000000',
			'outline': "#000000",
			'background': '#FFFFFF'
		}
		if generate_graph(modems_dict):
			return {"status": "graph", "filename": modems_dict['filename']}
		else:
			return {"status": "text", "text": text}
	except Exception as e:
		return {"status": "error", "text": e}
		
def get_random_filename(n):
	abc ='abcdefghijklmnopqrstuvwxyzQWERTYUIOPASDFGHJKLZXCVBNM0123456789_-'
	filename = ''
	while len(filename) < n:
		filename += abc[random.randrange(0, len(abc), 1)]
	return filename

def generate_graph(modems_dict):
	
	font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 12)
	
	img_height = (modems_dict['modems_count']*25)+15+15+modems_dict['offset_size']
	
	img = Image.new('RGB', (300, img_height), modems_dict['background'])
	imgDrawer = ImageDraw.Draw(img)
	
	y = 10
	
	for modem in modems_dict['modems']:
		dbm = modem.dbm
		imgDrawer.rectangle((10, y, (250 + int(dbm)), y+15), fill=modem.fill_color, outline=modems_dict['outline'])
		if (dbm == -140):
			dbm = "∞"
		imgDrawer.text((12, y+1), str(modem.name) + ": " + str(dbm), fill=modem.text_color, font=font)
		y += 25
		
	imgDrawer.text((10, y), get_today(), fill=modems_dict['main_text_color'], font=font)
	y += 15
	for txt in modems_dict['response_text']:
		if (txt == "Status of SMSD: smsd is NOT running."):
			imgDrawer.text((10, y), txt, fill="#FF0000", font=font)
		else:
			imgDrawer.text((10, y), txt, fill=modems_dict['main_text_color'], font=font)
		y += 15
	try:		
		img.save(modems_dict['filename'])
		return True
	except Exception as e:
		return False

def start_sms_service():
	subprocess.call("/etc/sms_service.sh")
