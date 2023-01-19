#!/usr/bin/env python
import configparser

import pika

creds = pika.PlainCredentials('irrigator', 'pogrogator1337')
pars = pika.ConnectionParameters(host='127.0.0.1', virtual_host='/', credentials=creds, socket_timeout=2)
conn = pika.BlockingConnection(pars)
chan = conn.channel()

chan.exchange_declare(exchange='config', exchange_type='fanout')

result = chan.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue

chan.queue_bind(exchange='config', queue=queue_name)

print(' [*] Waiting for config. To exit press CTRL+C')


def modify_csv(ch, method, properties, body):
    print(f" [x] Config: {body.decode('utf-8')}")
    target_humidity = body.decode('utf-8')

    config = configparser.ConfigParser()
    config.read('../data/settings.ini')
    config['DEFAULT']['target_humidity'] = target_humidity
    with open('../data/settings.ini', 'w') as f:
        config.write(f)


chan.basic_consume(queue=queue_name, on_message_callback=modify_csv, auto_ack=True)

chan.start_consuming()
