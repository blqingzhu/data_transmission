import json
import requests

from common.csvfile import create_csv, append_csv
from common.random_common import random_string
from interface.common.login import admin_login

typeCode_list = {"有人摊铺机": 104, "无人压路机": 202, "有人压路机": 103, "单缸压路机": 1031, "双缸压路机": 1032, "胶轮压路机": 1033}

admin_http_pex = 'http://47.105.124.12:84/'
admin_headers = {"Accept": "application/json,text/plain,*/*",
                 'Referer': 'http://47.105.124.12:84/',
                 'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; InfoPath.3)',
                 'Content-Type': 'application/json;charset=UTF-8'
                 }
# 创建设备
addDevice = admin_http_pex + "api/iot-base-server/v2/system/deviceBaseInfo/add"
# 创建终端
addTerminal = admin_http_pex + "api/iot-base-server/v2/system/terminal/add"

# 查找厂商产品型号
DeviceModel = admin_http_pex + "api/iot-base-server/v2/system/public/code/getModelList"


def findDeviceModel(DeviceModel,typeCode, DeviceModelName,admin_headers):
    """查找厂商产品型号
       :return:
    """

    payload = {"typeCode": str(typeCode)}
    r = requests.post(DeviceModel, data=json.dumps(payload), headers=admin_headers)
    r.encoding = 'utf-8'
    result = r.json()
    data = result['data']
    for i in data:
        if i['name'] == DeviceModelName:
            modelId = i['id']
            return modelId
    return ""


def devices(addDevice, admin_headers, deviceName, deviceCode, modelId):
    """创建设备
     :return:
  """

    payload = {'deviceName': deviceName, 'deviceCode': deviceCode, 'engineCode': '032584', 'controllerCode': '342871',
               'typeCode': '104', 'modelId': modelId, 'fromType': 1, 'openStatus': 0, 'contactPhone': '13526212021',
               'depreciateMoney': '123', 'driverMoney': '12', 'serviceDays': '345'}
    print(payload)

    r = requests.post(addDevice, data=json.dumps(payload), headers=admin_headers)

    r.encoding = 'utf-8'
    result = r.json()
    return


def Terminal(addTerminal, admin_headers, deviceCode1):
    """创建终端
           :return:
        """

    terminalId = random_string()
    terminalCode = random_string()
    payload = {"terminalId": terminalId, "terminalCode": terminalCode, "deviceCode": deviceCode1}
    print(payload)

    r = requests.post(addTerminal, data=json.dumps(payload), headers=admin_headers)
    r.encoding = 'utf-8'
    result = r.json()
    if result['code'] == '0':
        create_csv("terminalId.csv")
        datas = [[terminalId]]
        append_csv("terminalId.csv", datas)


if __name__ == '__main__':

    result = admin_login(admin_headers)
    admin_headers = result['admin_headers']
    DeviceModelName = "有人摊铺机"
    typeCode = typeCode_list.get(DeviceModelName)

    modelId = findDeviceModel(DeviceModel,typeCode, DeviceModelName,admin_headers)
    for i in range(1):
        deviceName = random_string()
        deviceCode = random_string()
        devices(addDevice, admin_headers, deviceName, deviceCode, modelId)
        Terminal(addTerminal, admin_headers, deviceCode)
