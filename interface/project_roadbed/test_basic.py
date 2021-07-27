import hashlib
import json
import random
import unittest
import requests
import os, sys

from faker import Faker

from common.random_common import random_string
from interface.common.login import companyLogin
from interface.global_var import global_var_model, roadbed_var
from utx import tag, Tag

parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parentdir)
fake = Faker(locale='zh_CN')


class test_basic(unittest.TestCase):
    ''' 企业用户注册 '''

    def setUp(self):
        # 登录
        # self.login = global_var_model.company_login
        # 获取项目
        self.company_ProjectList = global_var_model.company_ProjectList
        # 添加工艺层级
        self.company_addLevel = roadbed_var.company_addLevel
        # 添加摊铺属性
        self.company_addStand = roadbed_var.company_addStand
        # 企业管理员账号
        self.company_admin_userName = global_var_model.company_admin_userName
        self.company_admin_password = global_var_model.company_admin_password
        self.company_admin_phone = global_var_model.company_admin_phone
        self.company_name = global_var_model.company_name
        self.company_name = global_var_model.company_name
        self.ProjecName = global_var_model.ProjecName
        self.headers = global_var_model.headers
        self.g = globals()

    def tearDown(self):
        print(self.result)

    @tag(Tag.SMOKE)
    def test_1_one(self):
        """登录
           :return:
        """
        self.result = companyLogin(self.company_admin_userName, self.company_admin_password, self.headers)
        self.g['test_1_one'] = self.result['code']
        self.g["companyCode"] = self.result['companyCode']
        self.assertEqual(self.result['status_code'], 200)
        self.assertEqual(self.result['msg'], 'success')
        self.assertEqual(self.result['code'], '0')

    @tag(Tag.SMOKE)
    def test_2_one(self):
        """获取项目
           :return:
        """
        if self.g['test_1_one'] != '0':
            result = '{"msg": "test_1_one用例失败"}'
            self.result = json.loads(result)
            self.skipTest("result")
        payload = {}
        r = requests.post(self.company_ProjectList, data=json.dumps(payload), headers=self.headers)
        r.encoding = 'utf-8'
        self.result = r.json()
        data = self.result['data']
        for i in data:
            if i['projectName'] == self.ProjecName:
                self.g['projectCode'] = i['projectCode']
                break
        self.headers['projectCode'] = self.g["projectCode"]
        self.g['test_2_one'] = self.result['code']
        self.assertEqual(r.status_code, 200)
        self.assertEqual(self.result['msg'], 'success')
        self.assertEqual(self.result['code'], '0')

    @tag(Tag.SMOKE)
    def test_3_one(self):
        """成功添加工艺层级
           :return:
        """
        if self.g['test_2_one'] != '0':
            result = '{"msg": "test_2_one用例失败"}'
            self.result = json.loads(result)
            self.skipTest("result")
        technologyLevel = random.randint(0, len(roadbed_var.technologyLevel) - 1)
        technologyName = roadbed_var.technologyLevel[technologyLevel]
        self.g['technologyName'] = technologyName
        print("工艺层级名称："+technologyName)
        payload = {"technologyName": technologyName, "technologyLevel": technologyLevel+1}
        r = requests.post(self.company_addLevel, data=json.dumps(payload), headers=self.headers)
        r.encoding = 'utf-8'
        self.result = r.json()
        self.g['technologyLevelCode'] = self.result['data']
        self.g['test_3_one'] = self.result['code']
        self.assertEqual(r.status_code, 200)
        self.assertEqual(self.result['msg'], 'success')
        self.assertEqual(self.result['code'], '0')

    @tag(Tag.SMOKE)
    def test_4_one(self):
        """添加摊铺属性
           :return:
        """
        if self.g['test_3_one'] != '0':
            result = '{"msg": "test_3_one用例失败"}'
            self.result = json.loads(result)
            self.skipTest("result")
        constructionTechnologyType = 0  # 摊铺
        technologyName = self.g['technologyName'] + "_摊铺_" + random_string()  # 属性名称
        pavingThickness = '1.5'  # 摊铺厚度
        pavingMinTemperature = '12'  # 摊铺最小温度
        pavingMaxTemperature = '13'  # 摊铺最大温度
        pavingMinSpeed = '15'  # 摊铺最小速度
        pavingMaxSpeed = '17'  # 摊铺最大速度
        isDefault = 0  # 是否默认 0-是；1-否
        payload = [{"technologyLevelCode": self.g['technologyLevelCode'],
                   "constructionTechnologyType": constructionTechnologyType, "technologyName": technologyName,
                   "pavingThickness": pavingThickness, "pavingMinTemperature": pavingMinTemperature,
                   "pavingMaxTemperature": pavingMaxTemperature, "pavingMinSpeed": pavingMinSpeed,
                   "pavingMaxSpeed": pavingMaxSpeed, "isDefault": isDefault}]
        r = requests.post(self.company_addStand, data=json.dumps(payload), headers=self.headers)
        r.encoding = 'utf-8'
        self.result = r.json()
        self.g['test_4_one'] = self.result['code']
        self.assertEqual(r.status_code, 200)
        self.assertEqual(self.result['msg'], 'success')
        self.assertEqual(self.result['code'], '0')

    @tag(Tag.SMOKE)
    def test_5_one(self):
        """添加压实属性
           :return:
        """
        if self.g['test_3_one'] != '0':
            result = '{"msg": "test_3_one用例失败"}'
            self.result = json.loads(result)
            self.skipTest("result")
        constructionTechnologyType = 1  # 压实
        technologyName = self.g['technologyName'] + "_压实_" + random_string()  # 属性名称
        firstPressurePercentage = '70'  # 初压最小达标百分比，压实度
        firstPressureMinTimes = '1'  # 初压最小遍数
        firstPressureMaxTimes = '2'  # 初压最大遍数
        secondPressurePercentage = '80'  # 复压最小达标百分比，压实度
        secondPressureMinTimes = '3'  # 复压最小遍数
        secondPressureMaxTimes = '6'  # 复压最大遍数
        finalPressurePercentage = '90'  # 终压最小达标百分比，压实度
        finalPressureMinTimes = '7'  # 终压最小遍数
        finalPressureMaxTimes = '9'  # 终压最大遍数
        isDefault = 0  # 是否默认 0-是；1-否
        payload = [{"technologyLevelCode": self.g['technologyLevelCode'],
                   "constructionTechnologyType": constructionTechnologyType, "technologyName": technologyName,
                   "firstPressurePercentage": firstPressurePercentage, "firstPressureMinTimes": firstPressureMinTimes,
                   "firstPressureMaxTimes": firstPressureMaxTimes, "secondPressurePercentage": secondPressurePercentage, "secondPressureMinTimes": secondPressureMinTimes,
                   "secondPressureMaxTimes": secondPressureMaxTimes, "finalPressurePercentage": finalPressurePercentage, "finalPressureMinTimes": finalPressureMinTimes,
                   "finalPressureMaxTimes": finalPressureMaxTimes, "isDefault": isDefault}]
        r = requests.post(self.company_addStand, data=json.dumps(payload), headers=self.headers)
        r.encoding = 'utf-8'
        self.result = r.json()
        self.g['test_5_one'] = self.result['code']
        self.assertEqual(r.status_code, 200)
        self.assertEqual(self.result['msg'], 'success')
        self.assertEqual(self.result['code'], '0')


if __name__ == '__main__':
    unittest.main()
