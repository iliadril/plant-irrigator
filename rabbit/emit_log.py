#!/usr/bin/env python

import pika
import sys
import logging

logging.basicConfig(level=logging.INFO)

creds = pika.PlainCredentials('irrigator', 'pogrogator1337')
pars = pika.ConnectionParameters(host='127.0.0.1', virtual_host='/', credentials=creds, socket_timeout=2)
pars = pika.URLParameters("amqp://irrigator:pogrogator1337@amqt.iliadril.xyz/%2f")
conn = pika.BlockingConnection(pars)
chan = conn.channel()

chan.exchange_declare(exchange='logs', exchange_type='fanout')

msg = ' '.join(sys.argv[1:]) or "info: Hello World!"
chan.basic_publish(exchange='logs', routing_key='', body=msg)
print(f" [x] Sent '{msg}'")
conn.close()
