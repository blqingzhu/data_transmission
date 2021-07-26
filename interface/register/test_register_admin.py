import hashlib
import json
import unittest
import requests
import os, sys
from functools import wraps
from requests.auth import HTTPBasicAuth
from unittest import skipIf

from cryptography.hazmat.primitives.hashes import MD5

from common.CreditIdentifie import get_code
from db_fixture.redis_db import Redis
from common.random_common import random_string, random_name_str, phoneNO, random_emil, converter

from faker import Faker

from interface import global_var_model
from utx import tag, utx, Tag

parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parentdir)
fake = Faker(locale='zh_CN')

send_captcha = False;  # 不发送短信


# 根据ASCII码的顺序加载测试用例，数字与字母的顺序为：0-9，A-Z，a-z
class test_register_admin(unittest.TestCase):
    ''' 企业管理员注册 '''

    def setUp(self):
        # 注册-获取验证码
        self.getmessage = global_var_model.getmessage
        # 注册-验证验证码
        self.checkMessage = global_var_model.checkMessage
        # 根据手机号获取用户信息
        self.getUser = global_var_model.getUser
        # 注册-添加用户
        self.addUser = global_var_model.addUser
        # 注册-提交审核
        self.coment = global_var_model.coment
        self.headers = global_var_model.headers
        # 管理后台登录
        self.login = global_var_model.login
        #获取菜单
        self.menu = global_var_model.menu
        # 添加角色
        self.roleAdd = global_var_model.roleAdd
        # 查找角色id
        self.findRole = global_var_model.findRole
        # 查找企业id
        self.findCompany = global_var_model.findCompany
        # 审核企业
        self.checkApplyCompany = global_var_model.checkApplyCompany
        self.admin_headers = global_var_model.admin_headers
        self.g = globals()
        self.admin_userName = global_var_model.admin_userName
        self.admin_password = global_var_model.admin_password  # 管理后台密码

    def tearDown(self):
        print(self.result)

    @tag(Tag.SMOKE)
    # 注册-获取验证码测试
    def test_1_one(self):
        """ 手机号获取验证：手机号正确 """
        telphone = fake.phone_number()  # 手机号
        print("手机号：" + telphone)
        payload = {'phone': telphone}
        self.g["telphone"] = telphone
        if send_captcha:
            r = requests.get(self.getmessage, params=payload, headers=self.headers)
            r.encoding = 'utf-8'
            self.result = r.json()
            self.g['test_1_one'] = self.result['code']
            self.assertEqual(r.status_code, 200)
            # self.assertEqual(self.result['data'], '验证码发送成功')
            # self.assertEqual(self.result['msg'], 'success')
            self.assertEqual(self.result['code'], '0')
        else:
            result = '{"msg": "跳过用例，不发送短信"}'
            self.result = json.loads(result)
            self.skipTest("result")

    @tag(Tag.SMOKE)
    def test_2_one(self):
        """
        手机号验证码输入：手机号和验证码正确
        """
        phone = self.g["telphone"]
        redis = Redis()
        captcha = redis.registerIDcode(phone)
        print("验证码：" + captcha)
        redis.close()
        payload = {"phone": phone, "captcha": captcha}
        self.headers['Cookie'] = 'registerphone=' + phone
        r = requests.post(self.checkMessage, data=json.dumps(payload), headers=self.headers)
        self.result = r.json()
        self.g['test_2_one'] = self.result['code']
        self.assertEqual(r.status_code, 200)
        self.assertEqual(self.result['msg'], 'success')
        self.assertEqual(self.result['code'], '0')

    @tag(Tag.SMOKE)
    def test_3_one(self):
        """ 成功添加用户： """
        if self.g['test_2_one'] != '0':
            result = '{"msg": "test_2_one用例失败"}'
            s = json.loads(result)
            print(s)
            self.result = json.loads(result)
            self.skipTest("result")
        userName = random_string()  # 用户名
        userPwd = fake.password(length=6, special_chars=False)  # 密码
        trueName = fake.name()  # 真实姓名
        userEmail = fake.company_email()  # 邮箱
        contact = self.g['telphone']  # 手机号
        print("用户名：" + userName)
        print("密码：" + userPwd)
        self.g["userName"] = userName
        self.g["trueName"] = trueName
        self.g["userPwd"] = userPwd
        self.g["userEmail"] = userEmail
        payload = {'userName': userName, 'userPwd': hashlib.md5(userPwd.encode()).hexdigest(), 'trueName': trueName,
                   'contact': contact, 'userEmail': userEmail}
        # headers['Referer'] = http_pex + 'registerf?phone=%s' % contact
        r = requests.post(self.addUser, data=json.dumps(payload), headers=self.headers)
        self.result = r.json()
        self.assertEqual(r.status_code, 200)
        self.assertEqual(self.result['msg'], 'success')
        self.assertEqual(self.result['code'], '0')

    @tag(Tag.SMOKE)
    def test_4_one(self):
        """ 成功提交审核： """
        if self.g['test_2_one'] != '0':
            result = '{"msg": "test_2_one用例失败"}'
            s = json.loads(result)
            print(s)
            self.result = json.loads(result)
            self.skipTest("result")
        name = fake.company()  # 企业名称
        companyNumber = get_code()  # 社会信用代码
        phone = self.g['telphone']  # 电话
        fileName = 't.png'  # 图片名称
        fileBase64 = converter(fileName)  # 图片的Base64格式
        companyUsername = self.g["userName"]  # 用户名
        companyEmail = self.g["userEmail"]  # 邮箱
        payload = {'name': name, 'companyNumber': companyNumber, 'phone': phone,
                   'fileName': fileName, 'fileBase64': 'data:image/png;base64,' + str(fileBase64),
                   'companyUsername': companyUsername,
                   'companyEmail': companyEmail}

        # headers['Referer'] = http_pex + 'thirdstepregister?name&companyNumber&phone=%s&userName=%s&userEmail=%s' % (
        #     phone, self.g["userName"], self.g["userEmail"])
        print("公司名称：" + name)
        r = requests.post(self.coment, data=json.dumps(payload), headers=self.headers)
        self.g["company"] = name
        self.result = r.json()
        self.assertEqual(r.status_code, 200)
        self.assertEqual(self.result['msg'], 'success')
        self.assertEqual(self.result['code'], '0')

    # def test_5_one(self):
    #     """ 根据手机号获取用户信息 """
    #     contact = self.g['telphone']  # 手机号
    #     payload = {'contact': contact}
    #     r = requests.get(self.getUser, params=payload, headers=headers)
    #     self.result = r.json()
    #     self.assertEqual(r.status_code, 200)
    #     self.assertEqual(self.result['msg'], 'success')
    #     self.assertEqual(self.result['code'], '0')

    @tag(Tag.SMOKE)
    def test_6_one(self):
        """登录
           :return:
        """
        payload = {'userName': self.admin_userName, 'password': hashlib.md5(self.admin_password.encode()).hexdigest()}
        r = requests.post(self.login, data=json.dumps(payload), headers=self.admin_headers)
        r.encoding = 'utf-8'
        self.result = r.json()
        data = self.result['data']
        self.g['test_6_one'] = self.result['code']
        self.g["admin_uid"] = data['uid']
        self.admin_headers['Cookie'] = 'Admin-Token=' + self.g["admin_uid"]
        self.admin_headers['uid'] = self.g["admin_uid"]
        self.assertEqual(r.status_code, 200)
        self.assertEqual(self.result['msg'], 'success')
        self.assertEqual(self.result['code'], '0')

    @tag(Tag.SMOKE)
    def test_7_one(self):
        """获取菜单
           :return:
        """
        if self.g['test_6_one'] != '0':
            result = '{"msg": "test_2_one用例失败"}'
            self.result = json.loads(result)
            self.skipTest("result")
        payload = {"parentId": "-1"}
        r = requests.post(self.menu, data=json.dumps(payload), headers=self.admin_headers)
        r.encoding = 'utf-8'
        self.result = r.json()
        menu_data = self.result['data']
        menu_code = []
        menu_code.append("-1")
        for i in menu_data:
            menu_code.append(i['menuCode'])
            a = i['children']
            if a:
                for j in range(len(a)):
                    menu_code.append(a[j]['menuCode'])

        self.g["menuList"] = menu_code

        self.assertEqual(r.status_code, 200)
        self.assertEqual(self.result['msg'], 'success')
        self.assertEqual(self.result['code'], '0')

    @tag(Tag.SMOKE)
    def test_8_one(self):
        """添加角色
                   :return:
                """
        if self.g['test_6_one'] != '0':
            result = '{"msg": "test_2_one用例失败"}'
            s = json.loads(result)
            print(s)
            self.result = json.loads(result)
            self.skipTest("result")
        rolename = self.g["company"] + "_超级管理员"
        print('角色名称：' + rolename)
        payload = {"roleName": rolename, "menuList": self.g["menuList"], "status": 1}
        # admin_headers['Cookie'] = 'Admin-Token=' + self.g["admin_uid"]
        # admin_headers[
        #     'secretkey'] = 'TEyqOSveuxBAp6tjHp2xyFXuuGL+J4EkZfhHoo29I/BGtYftKUhhJWCR8RaU3o6NW1nPLcZdhhp4GtKyYjuwvA=="'
        # admin_headers['uid'] = self.g["admin_uid"]
        self.g["rolename"] = rolename
        r = requests.post(self.roleAdd, data=json.dumps(payload), headers=self.admin_headers)
        r.encoding = 'utf-8'
        self.result = r.json()

        self.assertEqual(r.status_code, 200)
        self.assertEqual(self.result['msg'], 'success')
        self.assertEqual(self.result['code'], '0')

    @tag(Tag.SMOKE)
    def test_9_one(self):
        """查找角色id
                                   :return:
                                """
        if self.g['test_6_one'] != '0':
            result = '{"msg": "test_2_one用例失败"}'
            s = json.loads(result)
            print(s)
            self.result = json.loads(result)
            self.skipTest("result")
        print(self.g["company"])
        payload = {"pageNo": 1, "pageSize": 10, "name": self.g["rolename"]}
        # admin_headers['Cookie'] = 'Admin-Token=' + self.g["admin_uid"]
        # admin_headers[
        #     'secretkey'] = 'TEyqOSveuxBAp6tjHp2xyFXuuGL+J4EkZfhHoo29I/BGtYftKUhhJWCR8RaU3o6NW1nPLcZdhhp4GtKyYjuwvA=="'
        # admin_headers['uid'] = self.g["admin_uid"]
        r = requests.post(self.findRole, data=json.dumps(payload), headers=self.admin_headers)
        r.encoding = 'utf-8'
        self.result = r.json()
        data = self.result['data']
        a = data['list']
        if a:
            for j in range(len(a)):
                b = a[j]['roleId']

        self.g["roleId"] = b
        self.assertEqual(r.status_code, 200)
        self.assertEqual(self.result['msg'], 'success')
        self.assertEqual(self.result['code'], '0')

    @tag(Tag.SMOKE)
    def test_10_one(self):
        """查找企业
                           :return:
                        """
        if self.g['test_6_one'] != '0':
            result = '{"msg": "test_2_one用例失败"}'
            s = json.loads(result)
            print(s)
            self.result = json.loads(result)
            self.skipTest("result")
        payload = {"pageNo": 1, "pageSize": 10, "applyCompanyName": self.g["company"]}
        # admin_headers['Cookie'] = 'Admin-Token=' + self.g["admin_uid"]
        # admin_headers[
        #     'secretkey'] = 'TEyqOSveuxBAp6tjHp2xyFXuuGL+J4EkZfhHoo29I/BGtYftKUhhJWCR8RaU3o6NW1nPLcZdhhp4GtKyYjuwvA=="'
        # admin_headers['uid'] = self.g["admin_uid"]
        r = requests.post(self.findCompany, data=json.dumps(payload), headers=self.admin_headers)
        r.encoding = 'utf-8'
        self.result = r.json()
        data = self.result['data']
        a = data['list']
        if a:
            for j in range(len(a)):
                b = a[j]['id']
        self.g["company_id"] = b
        self.assertEqual(r.status_code, 200)
        self.assertEqual(self.result['msg'], 'success')
        self.assertEqual(self.result['code'], '0')

    @tag(Tag.SMOKE)
    def test_11_one(self):
        """审核企业
                                   :return:
                                """
        if self.g['test_6_one'] != '0':
            result = '{"msg": "test_2_one用例失败"}'
            s = json.loads(result)
            print(s)
            self.result = json.loads(result)
            self.skipTest("result")
        payload = {"id": self.g["company_id"], "auditType": 1, "roleId": self.g["roleId"]}
        # admin_headers['Cookie'] = 'Admin-Token=' + self.g["admin_uid"]
        # admin_headers[
        #     'secretkey'] = 'TEyqOSveuxBAp6tjHp2xyFXuuGL+J4EkZfhHoo29I/BGtYftKUhhJWCR8RaU3o6NW1nPLcZdhhp4GtKyYjuwvA=="'
        # admin_headers['uid'] = self.g["admin_uid"]
        r = requests.post(self.checkApplyCompany, data=json.dumps(payload), headers=self.admin_headers)
        r.encoding = 'utf-8'
        self.result = r.json()
        self.assertEqual(r.status_code, 200)
        self.assertEqual(self.result['msg'], 'success')
        self.assertEqual(self.result['code'], '0')


if __name__ == '__main__':
    # test_data.init_data()  # 初始化接口测试数据
    unittest.main()
    # testsuite = unittest.TestSuite()
    # testsuite.addTest(register_admin_test("test_6_one"))
    # testsuite.addTest(register_admin_test("test_7_one"))
    # testsuite.addTest(register_admin_test("test_3_one"))
    # testsuite.addTest(register_admin_test("test_4_one"))
    # testsuite.addTest(register_admin_test("test_4_one"))
    # runner = unittest.TextTestRunner()
    # runner.run(testsuite)
