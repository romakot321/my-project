#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket

b = 6

sock = socket.socket()

textboxValue = b'hi'
sock.connect(('192.168.0.12', 9090))
sock.send((textboxValue))
sock.close()