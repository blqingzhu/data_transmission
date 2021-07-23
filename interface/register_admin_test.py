import unittest
import requests
import os, sys

from interface.random_common import random_string, random_name_str, phoneNO, random_emil

parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parentdir)
from db_fixture import test_data

http_pex = 'http://47.105.124.12:86/'


class register_admin_test(unittest.TestCase):
    ''' 企业管理员注册 '''

    def setUp(self):
        self.base_url = http_pex+"/iot-device/v1/manage/system/company/addUser"

    def tearDown(self):
        print(self.result)

    # def test_add_event_all_null(self):
    #     """ 所有参数为空 """
    #     payload = {'userName': '','userPwd': '', 'trueName': "", 'contact': '','userEmail': ''}
    #     r = requests.post(self.base_url, data=payload)
    #     self.result = r.json()
    #     self.assertEqual(self.result['status'], 10021)
    #     self.assertEqual(self.result['message'], 'parameter error')
    #
    # def test_add_event_eid_exist(self):
    #     """ 用户名已经存在 userName"""
    #     payload = {'eid': 1, 'name': '一加4发布会', 'limit': 2000, 'address': "深圳宝体", 'start_time': '2017'}
    #     r = requests.post(self.base_url, data=payload)
    #     self.result = r.json()
    #     self.assertEqual(self.result['status'], 10022)
    #     self.assertEqual(self.result['message'], 'event id already exists')
    #
    # def test_add_event_name_exist(self):
    #     """ 手机号已经存在 contact"""
    #     payload = {'eid': 11, 'name': '红米Pro发布会', 'limit': 2000, 'address': "深圳宝体", 'start_time': '2017'}
    #     r = requests.post(self.base_url, data=payload)
    #     self.result = r.json()
    #     self.assertEqual(self.result['status'], 10023)
    #     self.assertEqual(self.result['message'], 'event name already exists')
    #
    # def test_add_event_data_type_error(self):
    #     """ 日期格式错误 """
    #     payload = {'userName': random_string(6), 'userPwd': '123456', 'trueName': "", 'contact': '','userEmail': ''}
    #     r = requests.post(self.base_url, data=payload)
    #     self.result = r.json()
    #     self.assertEqual(self.result['code'], 0)
    #     self.assertIn('success', self.result['message'])

    def test_add_event_success(self):
        """ 添加成功 """
        payload = {'userName': random_string(), 'userPwd': '123456', 'trueName': random_name_str(), 'contact': phoneNO(),'userEmail': random_emil()}
        print(payload)

        r = requests.post(self.base_url, data=payload)
        print(r)
        self.result = r.json()
        self.assertEqual(self.result['status'], 200)
        self.assertEqual(self.result['message'], 'add event success')


if __name__ == '__main__':
    # test_data.init_data()  # 初始化接口测试数据
    unittest.main()
