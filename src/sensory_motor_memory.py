#! /usr/bin/env python

from random import choice
from sys import argv

import lidapy
from lidapy import LIDAThread, Config

action_topic = lidapy.Topic('actions')

actions = ['LEFT', 'RIGHT', 'DOWN', 'ROTATE']


def send_action():
    action = choice(actions)
    action_topic.send(action)


# Initialize the lidapy framework
lidapy.init(config=Config(argv[1]), process_name='sensory_motor_memory')
LIDAThread(name='sensory_motor_memory', callback=send_action).start()
