import hashlib
import json
import random
import unittest
import requests
import os, sys

from common.random_common import random_string

from faker import Faker

from interface.global_var import global_var_model
from utx import tag, Tag

parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parentdir)
fake = Faker(locale='zh_CN')


# 根据ASCII码的顺序加载测试用例，数字与字母的顺序为：0-9，A-Z，a-z
class test_register_project(unittest.TestCase):
    ''' 企业：创建项目 '''

    def setUp(self):
        """管理后台"""
        # 登录
        self.login = global_var_model.login
        # 企业列表查找企业
        self.findCheckedCompany = global_var_model.findCheckedCompany
        # 企业列表查找设备
        self.findBindDevicePage = global_var_model.findBindDevicePage
        # 数据授权
        self.bindTerminal = global_var_model.bindTerminal
        # 管理后台账号
        self.admin_userName = global_var_model.admin_userName
        self.admin_password = global_var_model.admin_password  # 管理后台密码
        self.admin_headers = global_var_model.admin_headers
        """服务后台"""
        # 登录
        self.company_login = global_var_model.company_login
        ## 获取项目类别
        self.company_ProjectType = global_var_model.company_ProjectType
        ## 获取省
        self.company_Province = global_var_model.company_Province
        ## 获取市
        self.company_City = global_var_model.company_City
        ## 获取单位company_Devices
        self.company_Units = global_var_model.company_Units
        ## 获取设备company_AddProject
        self.company_Devices = global_var_model.company_Devices
        #创建项目
        self.company_AddProject = global_var_model.company_AddProject
        # 企业管理员账号
        self.company_admin_userName = global_var_model.company_admin_userName
        self.company_admin_password = global_var_model.company_admin_password
        self.company_admin_phone = global_var_model.company_admin_phone
        self.company_name = global_var_model.company_name
        self.headers = global_var_model.headers
        self.ProjectTypeName = global_var_model.ProjectTypeName
        self.g = globals()

    def tearDown(self):
        print(self.result)

    # @tag(Tag.SMOKE)
    # def test_1_one(self):
    #     """管理后台：登录
    #        :return:
    #     """
    #     payload = {'userName': self.admin_userName, 'password': hashlib.md5(self.admin_password.encode()).hexdigest()}
    #     r = requests.post(self.login, data=json.dumps(payload), headers=self.admin_headers)
    #     r.encoding = 'utf-8'
    #     self.result = r.json()
    #     data = self.result['data']
    #     self.g['test_1_one'] = self.result['code']
    #     self.g["admin_uid"] = data['uid']
    #     self.admin_headers['Cookie'] = 'Admin-Token=' + self.g["admin_uid"]
    #     self.admin_headers['uid'] = self.g["admin_uid"]
    #     self.assertEqual(r.status_code, 200)
    #     self.assertEqual(self.result['msg'], 'success')
    #     self.assertEqual(self.result['code'], '0')
    #
    # @tag(Tag.SMOKE)
    # def test_2_one(self):
    #     """管理后台：查找需授权企业
    #        :return:
    #     """
    #     if self.g['test_1_one'] != '0':
    #         result = '{"msg": "test_1_one用例失败"}'
    #         self.result = json.loads(result)
    #         self.skipTest("result")
    #     payload = {"pageNo": 1, "pageSize": 10, "name": self.company_name}
    #     r = requests.post(self.findCheckedCompany, data=json.dumps(payload), headers=self.admin_headers)
    #     r.encoding = 'utf-8'
    #     self.result = r.json()
    #     data = self.result['data']['list']
    #     for i in data:
    #         if i['name'] == self.company_name:
    #             self.g['code'] = i['code']
    #     self.g['test_2_one'] = self.result['code']
    #     self.assertEqual(r.status_code, 200)
    #     self.assertEqual(self.result['msg'], 'success')
    #     self.assertEqual(self.result['code'], '0')
    #
    # @tag(Tag.SMOKE)
    # def test_3_one(self):
    #     """管理后台：查找未授权设备
    #        :return:
    #     """
    #     if self.g['test_2_one'] != '0':
    #         result = '{"msg": "test_2_one用例失败"}'
    #         self.result = json.loads(result)
    #         self.skipTest("result")
    #     payload = {"pageNo": 1, "pageSize": 10, "code": self.g['code'], "empowerStatus": 0}
    #     r = requests.post(self.findBindDevicePage, data=json.dumps(payload), headers=self.admin_headers)
    #     r.encoding = 'utf-8'
    #     self.result = r.json()
    #     data = self.result['data']['list']
    #     deviceCodelist = []
    #     for i in data:
    #         deviceCodelist.append(i['deviceCode'])
    #     self.g['deviceCodeList'] = deviceCodelist
    #     self.g['test_3_one'] = self.result['code']
    #     self.assertEqual(r.status_code, 200)
    #     self.assertEqual(self.result['msg'], 'success')
    #     self.assertEqual(self.result['code'], '0')
    #
    # @tag(Tag.SMOKE)
    # def test_4_one(self):
    #     """管理后台：数据授权
    #        :return:
    #     """
    #     if self.g['test_3_one'] != '0':
    #         result = '{"msg": "test_3_one用例失败"}'
    #         self.result = json.loads(result)
    #         self.skipTest("result")
    #     payload = {"code": self.g['code'], "list": self.g['deviceCodeList']}
    #     r = requests.post(self.bindTerminal, data=json.dumps(payload), headers=self.admin_headers)
    #     r.encoding = 'utf-8'
    #     self.result = r.json()
    #     self.g['test_4_one'] = self.result['code']
    #     self.assertEqual(r.status_code, 200)
    #     self.assertEqual(self.result['msg'], 'success')
    #     self.assertEqual(self.result['code'], '0')

    @tag(Tag.SMOKE)
    def test_5_one(self):
        """服务平台：登录
           :return:
        """
        payload = {'name': self.company_admin_userName,
                   'passwd': hashlib.md5(self.company_admin_password.encode()).hexdigest()}
        r = requests.post(self.company_login, data=json.dumps(payload), headers=self.admin_headers)
        r.encoding = 'utf-8'
        self.result = r.json()
        data = self.result['data']
        self.g['test_5_one'] = self.result['code']
        self.g["admin_uid"] = data['uid']
        self.g["companyCode"] = data['companyCode']
        self.g["admin_userSign"] = data['userSign']
        self.g["roleType"] = data['roleType']
        self.headers[
            'Cookie'] = 'Admin-Token=%s; userName=%s; passwd=%s; headerName=%s; roleType=%s; companyCode=%s; projectCode=null; registerphone=%s; uid=%s; userSign=%s' % (
            self.g["admin_uid"], self.company_admin_userName, self.company_admin_password, self.company_admin_userName,
            self.g["roleType"], self.g["companyCode"], self.company_admin_phone, self.g["admin_uid"],
            self.g["admin_userSign"])
        self.headers['roleType'] = str(self.g["roleType"])
        self.headers['companyCode'] = self.g["companyCode"]
        self.headers['projectCode'] = 'null'
        self.headers['uid'] = self.g["admin_uid"]
        self.assertEqual(r.status_code, 200)
        self.assertEqual(self.result['msg'], 'success')
        self.assertEqual(self.result['code'], '0')

    @tag(Tag.SMOKE)
    def test_6_one(self):
        """获取项目类别
           :return:
        """
        if self.g['test_5_one'] != '0':
            result = '{"msg": "test_5_one用例失败"}'
            self.result = json.loads(result)
            self.skipTest("result")
        payload = {}
        r = requests.post(self.company_ProjectType, data=json.dumps(payload), headers=self.headers)
        r.encoding = 'utf-8'
        self.result = r.json()
        print(self.result)
        data = self.result['data']
        for i in data:
            if i['typeName'] == self.ProjectTypeName:
                self.g['projectType'] = i['id']
        self.g['test_6_one'] = self.result['code']
        self.assertEqual(r.status_code, 200)
        self.assertEqual(self.result['msg'], 'success')
        self.assertEqual(self.result['code'], '0')

    @tag(Tag.SMOKE)
    def test_7_one(self):
        """获取省
           :return:
        """
        if self.g['test_5_one'] != '0':
            result = '{"msg": "test_5_one用例失败"}'
            self.result = json.loads(result)
            self.skipTest("result")
        payload = {}
        r = requests.post(self.company_Province, data=json.dumps(payload), headers=self.headers)
        r.encoding = 'utf-8'
        self.result = r.json()
        data = self.result['data']
        ProvinceInfo=data[random.randint(0, len(data)-1)]
        self.g['provinceCode']=ProvinceInfo['provinceCode']
        self.g['test_7_one'] = self.result['code']
        self.assertEqual(r.status_code, 200)
        self.assertEqual(self.result['msg'], 'success')
        self.assertEqual(self.result['code'], '0')

    @tag(Tag.SMOKE)
    def test_8_one(self):
        """获取市
           :return:
        """
        if self.g['test_7_one'] != '0':
            result = '{"msg": "test_7_one用例失败"}'
            self.result = json.loads(result)
            self.skipTest("result")
        payload = {"provinceCode": self.g['provinceCode']}
        r = requests.post(self.company_City, data=json.dumps(payload), headers=self.headers)
        r.encoding = 'utf-8'
        self.result = r.json()
        data = self.result['data']
        if len(data)!=0:
            CityInfo=data[random.randint(0, len(data)-1)]
            self.g['cityCode'] = CityInfo['cityCode']
        else: self.g['cityCode'] = ''
        self.g['test_8_one'] = self.result['code']
        self.assertEqual(r.status_code, 200)
        self.assertEqual(self.result['msg'], 'success')
        self.assertEqual(self.result['code'], '0')



    @tag(Tag.SMOKE)
    def test_9_one(self):
        """获取单位
           :return:
        """
        if self.g['test_5_one'] != '0':
            result = '{"msg": "test_5_one用例失败"}'
            self.result = json.loads(result)
            self.skipTest("result")
        payload = {"constructUnitsName":""}
        r = requests.post(self.company_Units, data=json.dumps(payload), headers=self.headers)
        r.encoding = 'utf-8'
        self.result = r.json()
        data = self.result['data']
        UnitsList=[]
        for i in data:
            for j in i['children']:
                UnitsList.append(j['unitsCode'])
        self.g['UnitsList'] = UnitsList
        self.g['test_9_one'] = self.result['code']
        self.assertEqual(r.status_code, 200)
        self.assertEqual(self.result['msg'], 'success')
        self.assertEqual(self.result['code'], '0')



    @tag(Tag.SMOKE)
    def test_10_one(self):
        """获取设备
           :return:
        """
        if self.g['test_5_one'] != '0':
            result = '{"msg": "test_5_one用例失败"}'
            self.result = json.loads(result)
            self.skipTest("result")
        payload = {"constructUnitsName":""}
        r = requests.get(self.company_Devices, params=payload, headers=self.headers)
        r.encoding = 'utf-8'
        self.result = r.json()
        data = self.result['data']
        DevicesList=[]
        for i in data:
            for j in i['child']:
                DevicesList.append(j['deviceCode'])
        self.g['DevicesList'] = DevicesList
        self.g['test_10_one'] = self.result['code']
        self.assertEqual(r.status_code, 200)
        self.assertEqual(self.result['msg'], 'success')
        self.assertEqual(self.result['code'], '0')



    @tag(Tag.SMOKE)
    def test_11_one(self):
        """创建项目
           :return:
        """
        if self.g['test_6_one'] != '0' or self.g['test_8_one'] != '0' or self.g['test_9_one'] != '0' or self.g['test_10_one'] != '0':
            result = '{"msg": "test_6_one用例失败|test_8_one用例失败|test_9_one用例失败|test_10_one用例失败"}'
            self.result = json.loads(result)
            self.skipTest("result")
        projectName="项目名称_"+random_string()
        payload = {"projectName":projectName,"projectType":self.g['projectType'] ,"buildSatus":0,"provinceCode":self.g['provinceCode'],"cityCode":self.g['cityCode'],"unitsCode":self.g['UnitsList'],"deviceCode":self.g['DevicesList']}
        r = requests.post(self.company_AddProject, data=json.dumps(payload), headers=self.headers)
        r.encoding = 'utf-8'
        self.result = r.json()
        self.g['test_11_one'] = self.result['code']
        self.assertEqual(r.status_code, 200)
        self.assertEqual(self.result['msg'], 'success')
        self.assertEqual(self.result['code'], '0')


if __name__ == '__main__':
    unittest.main()
