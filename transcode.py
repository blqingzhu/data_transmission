#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# -*- 数据转换 -*-
import binascii
import json
import re
import string
from functools import reduce
from locale import atoi

from send import sendsocket


# convert string to hex
def toBytes(s):
    a = str(s)
    b = "".join("{:02x}".format(ord(c)) for c in a)
    a_bytes = bytes.fromhex(b)
    len_content = str(hex(int(len(a_bytes)))).replace("0x", "").zfill(4)
    len_content = bytes.fromhex(len_content)  # 字符串变字符型字节流
    return len_content + a_bytes


# 判断括号是否成对出现且顺序合法
def find_last(string, str):
    last_position = -1
    while True:
        position = string.find(str, last_position + 1)
        if position == -1:
            return last_position
        last_position = position


# 匹配返回
def toJson(s):
    s = str(s)
    print(s)
    s = s[find_last(s, '{'):]
    print(s)
    p1 = re.compile(r'[{](.*?)[}]', re.S)  # 最小匹配
    p2 = re.compile(r'[{](.*)[}]', re.S)  # 贪婪匹配
    result = re.findall(p1, s)
    if len(result) >= 1:
        print(len(result))
        print(result[len(result) - 1])

        rejson = "{" + result[len(result) - 1] + "}"
        print(rejson)

        return json.loads(rejson)
    else:
        print('')
    # print(re.findall(p1, string))

# if __name__ == '__main__':
#
