#!/usr/bin/env python

import sys

import pika


def send_message(exchange_name: str, message: str):
    creds = pika.PlainCredentials('irrigator', 'pogrogator1337')
    pars = pika.ConnectionParameters(host='127.0.0.1', virtual_host='/', credentials=creds, socket_timeout=2)
    conn = pika.BlockingConnection(pars)
    chan = conn.channel()

    chan.exchange_declare(exchange=exchange_name, exchange_type='fanout')
    chan.basic_publish(exchange=exchange_name, routing_key='', body=bytes(message))
    conn.close()


if __name__ == "__main__":
    msg = ' '.join(sys.argv[1:]) or "info: Hello World!"
    send_message('logs', msg)
    print(f" [x] Sent '{msg}'")

