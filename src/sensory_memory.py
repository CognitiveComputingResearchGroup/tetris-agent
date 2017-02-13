#! /usr/bin/env python

from PIL import Image
from StringIO import StringIO
from sys import argv

import lidapy
from lidapy import LIDAThread, Config
from sensor_msgs.msg import CompressedImage

image_topic = lidapy.Topic('images', msg_type=CompressedImage)


def receive_image():
    msg = image_topic.receive()  # type: CompressedImage
    if msg:
        # TODO: Create the pixel layer from this image's data
        image = Image.open(StringIO(msg.data))


# Initialize the lidapy framework
lidapy.init(config=Config(argv[1]), process_name='sensory_memory')
LIDAThread(name='sensory_memory', callback=receive_image).start()
