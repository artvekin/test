#!/usr/bin/python3.5
# -*- coding: utf-8 -*-
import config
from sys import path
WEBHOOK_HOST = config.host
WEBHOOK_PORT = config.port  # 443, 80, 88 или 8443 (порт должен быть открыт!)
WEBHOOK_LISTEN = config.ip  # На некоторых серверах придется указывать такой же IP, что и выше

WEBHOOK_SSL_CERT = '/var/mimibot/webhook_cert.pem'  # Путь к сертификату
WEBHOOK_SSL_PRIV = '/var/mimibot/webhook_pkey.pem'  # Путь к приватному ключу

WEBHOOK_URL_BASE = "https://%s:%s" % (WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/%s/" % (config.token)
