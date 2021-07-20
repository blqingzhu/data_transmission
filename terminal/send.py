#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# -*- 发送接收tcp -*-
from socket import *

HOST = '118.190.145.250'

PORT = 2400

BUFFSIZE = 2048

ADDR = (HOST, PORT)


def sendsocket(content):
    tctimeClient = socket(AF_INET, SOCK_STREAM)
    try:
        tctimeClient.connect(ADDR)  # 连接Gateway服务器
    except Exception as e:
        print("connect excepiton: ")
        print(e)
    # a = b'\xAA\xBB\x01'

    # data = struct.pack("%dB" % (len(a)), *a)
    while True:
        # data = input(">")

        # if not data:
        # break
        # tctimeClient.send(data.encode())
        tctimeClient.send(content)  # .encode()
        # time.sleep(10)
        try:
            data = tctimeClient.recv(2048)
        except Exception as e:
            print(e)
        if not data:
            print("Link Disconnect!")
            break
        break
    return data


# socket关闭
def client_close(Client):
    Client.close()


if __name__ == "__main__":
    sendsocket()
