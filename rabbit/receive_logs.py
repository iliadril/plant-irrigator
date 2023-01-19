#!/usr/bin/env python

import pika


creds = pika.PlainCredentials('irrigator', 'pogrogator1337')
pars = pika.ConnectionParameters(host='127.0.0.1', virtual_host='/', credentials=creds, socket_timeout=2)
conn = pika.BlockingConnection(pars)
chan = conn.channel()

chan.exchange_declare(exchange='logs', exchange_type='fanout')

result = chan.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue

chan.queue_bind(exchange='logs', queue=queue_name)

print(' [*] Waiting for logs. To exit press CTRL+C')


def callback(ch, method, properties, body):
    print(f" [x] {body.decode('utf-8')}")


chan.basic_consume(
    queue=queue_name, on_message_callback=callback, auto_ack=True)

chan.start_consuming()
