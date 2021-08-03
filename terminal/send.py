#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# -*- 发送接收tcp -*-
from socket import *
import struct
import time

# HOST = '118.190.145.250'
#
# PORT = 2400
from os.path import abspath, dirname
import configparser as cparser
# ======== 读取db_config.ini 文件配置 ===========

base_dir =dirname(abspath(__file__))
base_dir = base_dir.replace('\\', '/')
file_path = base_dir + "/socket_config.ini"
cf = cparser.ConfigParser()
cf.read(file_path)
HOST = cf.get("config", "HOST")
PORT = int(cf.get("config", "PORT"))
BUFFSIZE =int( cf.get("config", "BUFFSIZE"))

# HOST='118.190.145.250'
# PORT=2400

# BUFFSIZE=2048


# ADDR = (HOST, PORT)


class socketClient():
    def __init__(self):
        self.ADDR = (HOST, PORT)
        tctimeClient = socket(AF_INET, SOCK_STREAM)

        self.tctimeClient = tctimeClient

    def socketconnect(self):
        try:
            self.tctimeClient.connect(self.ADDR)  # 连接Gateway服务器
            print("socket连接")
        except Exception as e:
            print("connect excepiton: ")
            print(e)


    def sendsocket(self, content):
        data=''
        self.tctimeClient.settimeout(5.0)
        while True:
            self.tctimeClient.send(content)
            try:
                data = self.tctimeClient.recv(BUFFSIZE)
            except Exception as e:
                print(e)
            if not data:
                # print("Link Disconnect!")
                break
            break
        return data

    # socket关闭
    def client_close(self):
        print("socket关闭")
        self.tctimeClient.close()


if __name__ == "__main__":
    # HOST = '118.190.145.250'
    # PORT = 2400
    Clientsocket = socketClient()
    Clientsocket.sendsocket(b'\xAA\xBB\x01')
    Clientsocket.client_close()
