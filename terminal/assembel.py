#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# -*- 按照协议要求组装数据 -*-
import binascii
import datetime
import codecs
import binascii
import time
from decimal import Decimal
from random import *
from random import randrange
from random import uniform
import re
# from lonlat import getDistance, getDegree, computerOffsetPosition
# from send import socketClient
# from transcode import toBytes, toJson
from db_fixture.terminal_data import select_data, update_termination_data, update_task_data, \
    insert_history_data, init_history_data
from terminal.lonlat import computerOffsetPosition, getDistance, getDegree
from terminal.send import socketClient
from terminal.transcode import toBytes, toJson

Header = "AABB"  # 帧头
Packet_type = ["03", "05"]  # 包类型
textArr = ['523003,5', '523003,3', '523003,4', '4340,3', '3363,5', '3363,4', '84,0', '1624,3']
interval_time = 10  # 终端上传间隔，单位s
flag_fault = False  # 不上传故障


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
    if steps == 1:
        print(stop - start)
        return [round(stop, 6)]
    else:
        return [start + round(float(i) * (stop - start), 6) / (float(steps) - 1) for i in range(steps)]


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


def jsondeal(didno, oil, hours, minlon, minlat, degree, distance, json_date):  # 转换消息体
    arr = []
    LongitudeLatitude = computerOffsetPosition(minlon, minlat, degree, distance)
    jsonstring1 = "{\"did\":\"" + didno + "\"}"
    jsonstring2 = portjson(didno, oil, hours, LongitudeLatitude[0], LongitudeLatitude[1], str(json_date))
    s_hex1 = toBytes(jsonstring1)
    s_hex2 = toBytes(jsonstring2)
    arr.append(s_hex1)
    arr.append(s_hex2)
    arr.append(str(LongitudeLatitude[0]) + ',' + str(LongitudeLatitude[1]))
    arr.append(jsonstring2)
    return arr


# 发送位置信息
def sendcontent(didno, minlon, minlat, degree, distance):
    mess = message()
    uptime = date()
    global oilConsume
    global workHours
    oilConsume = randomFloat(oilConsume, oilConsume + 2, 2)
    workHours = workHours + interval_time / 3600
    oil = str(oilConsume)
    hours = str(workHours)
    jsoncode = jsondeal(didno, oil, hours, minlon, minlat, degree, distance, uptime)
    '''
      帧头+包类型+消息ID+消息体（消息长度+消息内容）--字符型字节流
    '''
    content1 = bytes.fromhex(Header + Packet_type[0] + mess) + jsoncode[0]
    Clientsocket = socketClient()
    Clientsocket.socketconnect()
    data1 = Clientsocket.sendsocket(content1)  # 需要发送的16进制数
    if not data1:
        print("服务器失去连接")
    else:
        code_result = toJson(data1)["code"]
        if code_result == 0:
            print("鉴权成功")
            content2 = bytes.fromhex(Header + Packet_type[1] + mess) + jsoncode[1]
            # print(content2)
            data2 = Clientsocket.sendsocket(content2)  # 需要发送的16进制数

            update_termination_data(jsoncode[2], termination_id, oil, hours, uptime)
        else:
            print("鉴权失败")
    test_json = jsoncode[3].replace("\"", "\\\"")
    init_history_data(task_id, test_json, 1)
    Clientsocket.client_close()


# 上传位置信息
def portjson(did, oil, hours, lon, lat, json_date):
    engineRpm = str(randomInt(100, 500))  # 发动机转速

    engineWaterTp = str(randomInt(90, 110))  # 发动机冷却液温度
    oilPressure = str(randomInt(4, 10))  # 机油压力
    systemVoltage = str(randomInt(10, 32))  # 系统电压
    systemVoltageState = str(randomInt(0, 1))  # 系统电压状态
    faultcode = str(randomText(textArr))  # 故障编码
    if flag_fault:  # 有故障
        json = "{\"did\":\"" + did + "\",\"ts\":\"" + json_date + "\",\"mid\":\"28\",\"category\":2,\"version\":\"v3.3\"," \
                                                                  "\"data\":{\"oilConsume\":" + oil + \
               ",\"systemVoltageState\":" + systemVoltageState + ",\"systemVoltage\":" + systemVoltage + ",\"engineRpm\":" + engineRpm + \
               ",\"oilPressure\":" + oilPressure + ",\"workHours\":" + hours + ",\"engineWaterTp\":" + engineWaterTp + \
               ",\"engineErrorCode\":\"" + faultcode + "\"" + \
               ",\"oilLevel\":36,\"lon\":" + str(lon) + ",\"lat\":" + str(lat) + "}}"
    else:
        json = "{\"did\":\"" + did + "\",\"ts\":\"" + json_date + "\",\"mid\":\"28\",\"category\":2,\"version\":\"v3.3\"," \
                                                                  "\"data\":{\"oilConsume\":" + oil + \
               ",\"systemVoltageState\":" + systemVoltageState + ",\"systemVoltage\":" + systemVoltage + ",\"engineRpm\":" + engineRpm + \
               ",\"oilPressure\":" + oilPressure + ",\"workHours\":" + hours + ",\"engineWaterTp\":" + engineWaterTp + \
               ",\"oilLevel\":36,\"lon\":" + str(lon) + ",\"lat\":" + str(lat) + "}}"

    # print(json)
    return json


def poport(didNo, lonlatlist, task_step):
    # print(lonlat)
    minlat = lonlatlist['minlat']
    # print(minlat)
    minlon = lonlatlist['minlon']
    # print(minlon)
    maxlat = lonlatlist['maxlat']
    # print(maxlat)
    maxlon = lonlatlist['maxlon']
    # print(maxlon)
    distance = getDistance(minlat, minlon, maxlat, maxlon)  # 计算距离
    degree = getDegree(minlat, minlon, maxlat, maxlon)  # 计算方位角
    distance_list = floatrange(0, distance, task_step)
    # print (distance_list)
    for i in distance_list:
        print("-----")
        # print(i)
        sendcontent(didNo, minlon, minlat, degree, i)
        print("休息%ss" % interval_time)
        time.sleep(interval_time)
    update_task_data(task_id, 2)


def main():
    result = select_data()
    for row in result:
        global task_id
        global termination_id
        task_id = row['task_id']
        task_step = row['step']
        termination_id = row['termination_id']
        task_lonlat = row['task_lonlat'].split(',')
        lon_lat = row['lon_lat'].split(',')
        global oilConsume
        global workHours
        oilConsume = row['oilConsume']
        workHours = row['workHours']
        lonlat_list = dict(minlon=float(lon_lat[0]), minlat=float(lon_lat[1]), maxlon=float(task_lonlat[0]),
                           maxlat=float(task_lonlat[1]))
        poport(termination_id, lonlat_list, task_step)


if __name__ == '__main__':
    # 最小经度、最大经度、最小纬度、最大纬度
    # did = '622458'
    # lonlatlist = [112.101536, 112.318859, 40.760664, 40.851358]
    # oilConsume = 3343.4  # 累计油耗
    # workHours = 453.34  # 累计工作时长
    # poport(did, oilConsume, workHours, lonlatlist)
    main()
    # uptime ='20210723142301020'
    # lonlatlist = [112.101536, 112.318859]
    # update_termination_data(lonlatlist, 1, 1, 1, uptime)
