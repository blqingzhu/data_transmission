import hashlib
import json
import unittest
import requests
import os, sys
from common.random_common import random_string, random_digits

from faker import Faker

from interface.global_var import global_var_model
from utx import tag,  Tag

parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parentdir)
fake = Faker(locale='zh_CN')


# 根据ASCII码的顺序加载测试用例，数字与字母的顺序为：0-9，A-Z，a-z
class test_register_device(unittest.TestCase):
    ''' 管理后台：设备创建 '''

    def setUp(self):
        # 管理后台登录
        self.login = global_var_model.login
        # 创建项目类别
        self.addProjectType = global_var_model.addProjectType
        # 查找项目类别
        self.findProjectType = global_var_model.findProjectType
        # 创建产品类别
        self.addProduct = global_var_model.addProduct
        # 查找产品类别addDeviceModel
        self.findProduct = global_var_model.findProduct
        # 创建厂商产品型号
        self.addDeviceModel = global_var_model.addDeviceModel
        # 查找厂商产品型号
        self.findDeviceModel = global_var_model.findDeviceModel
        # 创建设备部件
        self.addDeviceParts = global_var_model.addDeviceParts
        # 查找设备部件
        self.findDeviceParts = global_var_model.findDeviceParts
        # 创建设备
        self.addDevice = global_var_model.addDevice
        # 查找设备addterminal
        self.findDevice = global_var_model.findDevice
        # 创建终端
        self.addTerminal = global_var_model.addTerminal
        # 企业管理员账号
        self.admin_headers = global_var_model.admin_headers
        self.admin_userName = global_var_model.admin_userName
        self.admin_password = global_var_model.admin_password  # 管理后台密码
        self.g = globals()

    def tearDown(self):
        print(self.result)

    @tag(Tag.SMOKE)
    def test_1_one(self):
        """登录
           :return:
        """
        payload = {'userName': self.admin_userName, 'password': hashlib.md5(self.admin_password.encode()).hexdigest()}
        r = requests.post(self.login, data=json.dumps(payload), headers=self.admin_headers)
        r.encoding = 'utf-8'
        self.result = r.json()
        data = self.result['data']
        self.g['test_1_one'] = self.result['code']
        self.g["admin_uid"] = data['uid']
        self.admin_headers['Cookie'] = 'Admin-Token=' + self.g["admin_uid"]
        self.admin_headers['uid'] = self.g["admin_uid"]
        self.assertEqual(r.status_code, 200)
        self.assertEqual(self.result['msg'], 'success')
        self.assertEqual(self.result['code'], '0')
        return self.g['admin_uid']

    @tag(Tag.SMOKE)
    def test_2_one(self):
        """创建项目类别
           :return:
        """
        if self.g['test_1_one'] != '0':
            result = '{"msg": "test_1_one用例失败"}'
            self.result = json.loads(result)
            self.skipTest("result")
        projectTypeName = "测试项目_" + random_string()
        projectTypeDesc = "项目类别描述"
        self.g["projectTypeName"] = projectTypeName
        payload = {"projectTypeName": projectTypeName, "projectTypeDesc": projectTypeDesc}
        print(payload)
        r = requests.post(self.addProjectType, data=json.dumps(payload), headers=self.admin_headers)
        r.encoding = 'utf-8'
        self.result = r.json()

        self.g['test_2_one'] = self.result['code']
        self.assertEqual(r.status_code, 200)
        self.assertEqual(self.result['msg'], 'success')
        self.assertEqual(self.result['code'], '0')

    @tag(Tag.SMOKE)
    def test_3_one(self):
        """查找项目类别
           :return:
        """
        if self.g['test_2_one'] != '0':
            result = '{"msg": "test_1_one用例失败"}'
            self.result = json.loads(result)
            self.skipTest("result")
        payload = {}
        r = requests.post(self.findProjectType, data=json.dumps(payload), headers=self.admin_headers)
        r.encoding = 'utf-8'
        self.result = r.json()
        data = self.result['data']
        for i in data:
            if i['typeName'] == self.g["projectTypeName"]:
                self.g["projectTypeCode"] = i['typeCode']
                break
        self.g['test_3_one'] = self.result['code']
        self.assertEqual(r.status_code, 200)
        self.assertEqual(self.result['msg'], 'success')
        self.assertEqual(self.result['code'], '0')

    @tag(Tag.SMOKE)
    def test_4_one(self):
        """创建产品类别
           :return:
        """
        if self.g['test_1_one'] != '0':
            result = '{"msg": "test_1_one用例失败"}'
            self.result = json.loads(result)
            self.skipTest("result")
        self.admin_headers['uid'] = self.g["admin_uid"]
        code = random_digits(6)
        productTypeName = "产品类别_" + random_string()
        productTypeDesc = "产品类别描述"
        self.g["productTypeName"] = productTypeName
        payload = {"code": code, "productTypeName": productTypeName, "productTypeDesc": productTypeDesc}
        r = requests.post(self.addProduct, data=json.dumps(payload), headers=self.admin_headers)
        r.encoding = 'utf-8'
        self.result = r.json()
        self.g['test_4_one'] = self.result['code']
        self.assertEqual(r.status_code, 200)
        self.assertEqual(self.result['msg'], 'success')
        self.assertEqual(self.result['code'], '0')

    @tag(Tag.SMOKE)
    def test_5_one(self):
        """查找产品类别
           :return:
        """
        if self.g['test_4_one'] != '0':
            result = '{"msg": "test_4_one用例失败"}'
            self.result = json.loads(result)
            self.skipTest("result")
        payload = {}
        r = requests.post(self.findProduct, data=json.dumps(payload), headers=self.admin_headers)
        r.encoding = 'utf-8'
        self.result = r.json()
        data = self.result['data']
        for i in data:
            if i['name'] == self.g["productTypeName"]:
                self.g["typeCode"] = i['code']
                break
        self.g['test_5_one'] = self.result['code']
        self.assertEqual(r.status_code, 200)
        self.assertEqual(self.result['msg'], 'success')
        self.assertEqual(self.result['code'], '0')

    @tag(Tag.SMOKE)
    def test_6_one(self):
        """创建厂商产品型号
           :return:
        """
        if self.g['test_1_one'] != '0':
            result = '{"msg": "test_1_one用例失败"}'
            self.result = json.loads(result)
            self.skipTest("result")
        self.admin_headers['uid'] = self.g["admin_uid"]
        DeviceModelName = "厂商产品型号_" + random_string()
        self.g["DeviceModelName"] = DeviceModelName
        payload = {"typeCode": self.g["typeCode"], "name": DeviceModelName, "factoryCode": "st", "modelType": 0, "modelStatus": 0}
        r = requests.post(self.addDeviceModel , data=json.dumps(payload), headers=self.admin_headers)
        r.encoding = 'utf-8'
        self.result = r.json()
        self.g['test_6_one'] = self.result['code']
        self.assertEqual(r.status_code, 200)
        self.assertEqual(self.result['msg'], 'success')
        self.assertEqual(self.result['code'], '0')

    @tag(Tag.SMOKE)
    def test_7_one(self):
        """查找厂商产品型号
           :return:
        """
        if self.g['test_6_one'] != '0':
            result = '{"msg": "test_6_one用例失败"}'
            self.result = json.loads(result)
            self.skipTest("result")
        payload ={"typeCode":self.g["typeCode"]}
        r = requests.post(self.findDeviceModel, data=json.dumps(payload), headers=self.admin_headers)
        r.encoding = 'utf-8'
        self.result = r.json()
        data = self.result['data']
        for i in data:
            if i['name'] == self.g["DeviceModelName"]:
                self.g["modelId"] = i['id']
                break
        self.g['test_7_one'] = self.result['code']
        self.assertEqual(r.status_code, 200)
        self.assertEqual(self.result['msg'], 'success')
        self.assertEqual(self.result['code'], '0')

    @tag(Tag.SMOKE)
    def test_8_one(self):
        """创建发动机设备部件
           :return:
        """
        if self.g['test_1_one'] != '0':
            result = '{"msg": "test_1_one用例失败"}'
            self.result = json.loads(result)
            self.skipTest("result")
        self.admin_headers['uid'] = self.g["admin_uid"]
        engineCode = random_digits(6)
        partsType=1#发动机
        partsFactory = "发动机部件厂商_"+random_string()
        partsModel = "发动机部件型号_"+random_string()
        self.g['engineCode']=engineCode
        payload = {"partsCode":engineCode,"partsType":partsType,"partsFactory":partsFactory,"partsModel":partsModel}
        r = requests.post(self.addDeviceParts , data=json.dumps(payload), headers=self.admin_headers)
        r.encoding = 'utf-8'
        self.result = r.json()
        self.g['test_8_one'] = self.result['code']
        self.assertEqual(r.status_code, 200)
        self.assertEqual(self.result['msg'], 'success')
        self.assertEqual(self.result['code'], '0')

    @tag(Tag.SMOKE)
    def test_9_one(self):
        """创建控制器设备部件
           :return:
        """
        if self.g['test_1_one'] != '0':
            result = '{"msg": "test_1_one用例失败"}'
            self.result = json.loads(result)
            self.skipTest("result")
        self.admin_headers['uid'] = self.g["admin_uid"]
        controllerCode = random_digits(6)
        partsType = 2  # 控制器
        partsFactory = "控制器部件厂商_" + random_string()
        partsModel = "控制器部件型号_" + random_string()
        self.g['controllerCode'] = controllerCode
        payload = {"partsCode": controllerCode, "partsType": partsType, "partsFactory": partsFactory,
                   "partsModel": partsModel}
        r = requests.post(self.addDeviceParts, data=json.dumps(payload), headers=self.admin_headers)
        r.encoding = 'utf-8'
        self.result = r.json()
        self.g['test_9_one'] = self.result['code']
        print(self.g['test_9_one'])
        self.assertEqual(r.status_code, 200)
        self.assertEqual(self.result['msg'], 'success')
        self.assertEqual(self.result['code'], '0')

    @tag(Tag.SMOKE)
    def test_10_one(self):
        """创建设备
           :return:
        """
        if self.g['test_5_one'] != '0' or self.g['test_7_one'] != '0' or self.g['test_8_one'] != '0' or self.g['test_9_one'] != '0':
            result = '{"msg": "test_5_one用例失败|test_7_one用例失败|test_8_one用例失败|test_9_one用例失败"}'
            self.result = json.loads(result)
            self.skipTest("result")
        deviceName = random_string()
        deviceCode= random_string()
        self.g['deviceCode']=deviceCode
        self.g['deviceName']=deviceName
        payload = {"deviceName":deviceName,"deviceCode":deviceCode,"engineCode":self.g['engineCode'],"controllerCode":self.g['controllerCode'],
                   "typeCode":self.g['typeCode'],"modelId":self.g['modelId'],"fromType":1,"openStatus":0,"contactPhone":"13526212021","depreciateMoney":"123","driverMoney":"12","serviceDays":"345"}
        r = requests.post(self.addDevice, data=json.dumps(payload), headers=self.admin_headers)
        r.encoding = 'utf-8'
        self.result = r.json()
        self.g['test_10_one'] = self.result['code']
        self.assertEqual(r.status_code, 200)
        self.assertEqual(self.result['msg'], 'success')
        self.assertEqual(self.result['code'], '0')

    @tag(Tag.SMOKE)
    def test_11_one(self):
        """创建终端
           :return:
        """
        if self.g['test_10_one'] != '0':
            result = '{"msg": "test_10_one用例失败"}'
            self.result = json.loads(result)
            self.skipTest("result")
        terminalId = random_string()
        terminalCode= random_string()
        payload = {"terminalId":terminalId,"terminalCode":terminalCode,"deviceCode":self.g['deviceCode']}
        print(payload)
        r = requests.post(self.addTerminal, data=json.dumps(payload), headers=self.admin_headers)
        r.encoding = 'utf-8'
        self.result = r.json()
        self.g['test_11_one'] = self.result['code']
        self.assertEqual(r.status_code, 200)
        self.assertEqual(self.result['msg'], 'success')
        self.assertEqual(self.result['code'], '0')




if __name__ == '__main__':
    unittest.main()
