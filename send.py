#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# -*- 发送接收tcp -*-
from socket import *
import struct
import time

HOST = '118.190.145.250'

PORT = 2400

BUFFSIZE = 2048

ADDR = (HOST, PORT)

tctimeClient = socket(AF_INET, SOCK_STREAM)

tctimeClient.connect(ADDR)

a = [0xAA, 0xBB, 0x01]
data = struct.pack("%dB" % (len(a)), *a)

while True:
    # data = input(">")

    # if not data:
    # break
    # tctimeClient.send(data.encode())
    tctimeClient.send(data)
    # time.sleep(10)
    data = tctimeClient.recv(1024)
    if not data:
        break
    print(data)
tctimeClient.close()