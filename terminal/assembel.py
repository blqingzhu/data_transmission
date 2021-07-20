#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# -*- 按照协议要求组装数据并发送 -*-
import datetime
from random import *
from random import randrange
from random import uniform
from terminal.lonlat import getDistance, getDegree, computerOffsetPosition
from terminal.send import sendsocket
from terminal.transcode import toBytes, toJson

Header = "AABB"  # 帧头
Packet_type = ["03", "05"]  # 包类型
textArr = ['523003,5', '523003,3', '523003,4', '4340,3', '3363,5', '3363,4', '84,0', '1624,3']


# 时间
def date():
    dt_ms = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')  # 含微秒的日期时间，来源 比特量化

    ts = str(dt_ms)[:-3]

    return ts


# 消息ID
def message():
    a = []
    s = ''
    for i in range(2):
        s = s + "".join([choice("0123456789ABCDEF") for i in range(2)])
    return s


# 生成递增随机距离
def floatrange(start, stop, steps):
    return [start + float(i) * (stop - start) / (float(steps) - 1) for i in range(steps)]


# 生成随机正整数
def randomInt(low, high):
    num = randrange(low, high)
    return num


# 生成随机正整数
def randomFloat(low, high, size):
    # 生成随机数，浮点类型
    a = uniform(low, high)
    # 控制随机数的精度round(数值，精度)
    return round(a, size)


# 随机取出数组中的一个
def randomText(Arr):
    length = len(Arr)
    if length < 1:
        return ''
    if length == 1:
        return str(textArr[0])
    randomNumber = randint(0, length - 1)
    return str(textArr[randomNumber])


def solution(s):
    # 创建存放最终结果的列表
    a = []
    # 判断字符串个数情况
    b = len(s)
    if b >= 2:
        if b % 2 == 0:
            for i in range(0, b, 2):
                a.append(s[i:i + 2])
            return a
        else:
            ss = s + '_'
            for i in range(0, b + 1, 2):
                a.append(ss[i:i + 2])
            return a
    else:
        if b == 1:
            ss = s + '_'
            for i in range(0, b + 1, 2):
                a.append(ss[i:i + 2])
            return a
        else:
            return a


def hexstr(ssend):
    st = []
    for i in ssend:
        byte = bytes.fromhex(i)
        st.append('%0x' % byte)
    print(st)
    return st


def jsondeal(didno, oil, hours, minlon, minlat, degree, distance):  # 转换消息体
    arr = []
    LongitudeLatitude = computerOffsetPosition(minlon, minlat, degree, distance)
    jsonstring1 = "{\"did\":\"" + did + "\"}"
    jsonstring2 = portjson(didno, oil, hours, LongitudeLatitude[0], LongitudeLatitude[1])
    s_hex1 = toBytes(jsonstring1)
    s_hex2 = toBytes(jsonstring2)
    arr.append(s_hex1)
    arr.append(s_hex2)
    return arr


# 发送位置信息
def sendcontent(didno, oil, hours, minlon, minlat, degree, distance):
    mess = message()
    jsoncode = jsondeal(didno, oil, hours, minlon, minlat, degree, distance)
    '''
      帧头+包类型+消息ID+消息体（消息长度+消息内容）--字符型字节流
    '''
    content1 = bytes.fromhex(Header + Packet_type[0] + mess) + jsoncode[0]
    data1 = sendsocket(content1)  # 需要发送的16进制数
    if not data1:
        print("服务器失去连接")
    else:
        code_result = toJson(data1)["code"]
        if code_result == 0:
            print("鉴权成功")
            content2 = bytes.fromhex(Header + Packet_type[1] + mess) + jsoncode[1]
            print(content2)
            sendsocket(content2)  # 需要发送的16进制数
        else:
            print("鉴权失败")


# 上传位置信息
def portjson(did, oil, hours, lon, lat):
    engineRpm = str(randomInt(100, 500))  # 发动机转速

    engineWaterTp = str(randomInt(90, 110))  # 发动机冷却液温度
    oilPressure = str(randomInt(4, 10))  # 机油压力
    systemVoltage = str(randomInt(10, 32))  # 系统电压
    systemVoltageState = str(randomInt(0, 1))  # 系统电压状态
    faultcode = str(randomText(textArr))  # 故障编码
    oilC = str(randomFloat(oil, oil + 2, 2))
    workH = str(randomFloat(hours, oil + 2, 2))
    json = "{\"did\":\"" + did + "\",\"ts\":\"" + str(date()) + "\",\"mid\":\"28\",\"category\":2,\"version\":\"v3.3\"," \
                                                                "\"data\":{\"oilConsume\":" + oilC + \
           ",\"systemVoltageState\":" + systemVoltageState + ",\"systemVoltage\":" + systemVoltage + ",\"engineRpm\":" + engineRpm + \
           ",\"oilPressure\":" + oilPressure + ",\"workHours\":" + workH + ",\"engineWaterTp\":" + engineWaterTp + \
           ",\"engineErrorCode\":\"" + faultcode + "\",\"oilLevel\":36,\"lon\":" + str(lon) + ",\"lat\":" + str(
        lat) + "}}"
    # print(json)
    return json


def poport(didNo, oil, hours, lonlat):
    # print(lonlat)
    minlat = lonlat[2]
    # print(minlat)
    minlon = lonlat[0]
    # print(minlon)
    maxlat = lonlat[3]
    # print(maxlat)
    maxlon = lonlat[1]
    # print(maxlon)
    distance = getDistance(minlat, minlon, maxlat, maxlon)  # 计算距离
    degree = getDegree(minlat, minlon, maxlat, maxlon)  # 计算方位角
    distance_list = floatrange(0, distance, 100)
    # print (distance_list)
    for i in distance_list:
        print("-----")
        # print(i)
        sendcontent(didNo, oil, hours, minlon, minlat, degree, i)



if __name__ == '__main__':
    # 最小经度、最大经度、最小纬度、最大纬度
    did = '622458'
    lonlatlist = [112.101536, 112.318859, 40.760664, 40.851358]
    oilConsume = 3343.4  # 累计油耗
    workHours = 453.34  # 累计工作时长
    poport(did, oilConsume, workHours, lonlatlist)
