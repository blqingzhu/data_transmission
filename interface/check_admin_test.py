import json
import unittest
import requests
import os, sys
from functools import wraps
from requests.auth import HTTPBasicAuth

from common.CreditIdentifie import get_code
from db_fixture.redis_db import Redis
from common.random_common import random_string, random_name_str, phoneNO, random_emil, converter

from faker import Faker

from terminal import GlobalVar

parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parentdir)
fake = Faker(locale='zh_CN')
http_pex = 'http://47.105.124.12:86/'
headers = {"Accept": "application/json,text/plain,*/*",
           'Referer': 'http://47.105.124.12:86/register',
           'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; InfoPath.3)',
           'Content-Type':'application/json;charset=UTF-8'
           }


def skip_dependon(depend=""):
    """
    :param depend: 依赖的用例函数名，默认为空
    :return: wraper_func
    """

    def wraper_func(test_func):
        @wraps(test_func)  # @wraps：避免被装饰函数自身的信息丢失
        def inner_func(self):
            if depend == test_func.__name__:
                raise ValueError("{} cannot depend on itself".format(depend))
            # print("self._outcome", self._outcome.__dict__)
            # 此方法适用于python3.4 +
            # 如果是低版本的python3，请将self._outcome.result修改为self._outcomeForDoCleanups
            # 如果你是python2版本，请将self._outcome.result修改为self._resultForDoCleanups
            failures = str([fail[0] for fail in self._outcome.result.failures])
            errors = str([error[0] for error in self._outcome.result.errors])
            skipped = str([error[0] for error in self._outcome.result.skipped])
            flag = (depend in failures) or (depend in errors) or (depend in skipped)
            if failures.find(depend) != -1:
                # 输出结果 [<__main__.TestDemo testMethod=test_login>]
                # 如果依赖的用例名在failures中，则判定为失败，以下两种情况同理
                # find()方法：查找子字符串，若找到返回从0开始的下标值，若找不到返回 - 1
                test = unittest.skipIf(flag, "{} failed".format(depend))(test_func)
            elif errors.find(depend) != -1:
                test = unittest.skipIf(flag, "{} error".format(depend))(test_func)
            elif skipped.find(depend) != -1:
                test = unittest.skipIf(flag, "{} skipped".format(depend))(test_func)
            else:
                test = test_func
            return test(self)

        return inner_func

    return wraper_func


# 根据ASCII码的顺序加载测试用例，数字与字母的顺序为：0-9，A-Z，a-z
class register_admin_test(unittest.TestCase):
    ''' 企业管理员注册 '''

    @classmethod
    def setUp(self):
        # 注册-获取验证码
        self.getmessage = http_pex + "api/iot-device/v1/manage/system/company/getmessage"
        # 注册-验证验证码
        self.checkMessage = http_pex + "api/iot-device/v1/manage/system/company/checkMessage"
        # 根据手机号获取用户信息
        self.getUser = http_pex + "api/v1/manage/system/company/getUser?"
        # 注册-添加用户
        self.addUser = http_pex + "api/iot-device/v1/manage/system/company/addUser"
        # 注册-提交审核
        self.coment = http_pex + "api/iot-device/v1/manage/system/company/coment"
        self.g = globals()

    def tearDown(self):
        print(self.result)

    # 注册-获取验证码测试
    def test_1_one(self):
        """ 手机号获取验证：手机号正确 """
        telphone = fake.phone_number()  # 手机号
        print("手机号："+telphone)
        payload = {'phone': telphone}
        r = requests.get(self.getmessage, params=payload, headers=headers)
        r.encoding = 'utf-8'
        self.g["telphone"] = telphone
        self.result = r.json()
        self.g["telphone_code"] = self.result['code']
        self.assertEqual(r.status_code, 200)
        # self.assertEqual(self.result['data'], '验证码发送成功')
        # self.assertEqual(self.result['msg'], 'success')
        self.assertEqual(self.result['code'], 0)

    def test_2_one(self):
        """ 手机号验证码输入：手机号和验证码正确 """
        phone=self.g["telphone"]
        code = self.g["telphone_code"]
        redis = Redis()
        captcha = redis.registerIDcode(code, phone)
        print("验证码："+captcha)
        redis.close()
        payload = {"phone": phone,"captcha":captcha}
        print( payload)
        headers['Cookie']='registerphone='+phone
        r = requests.post(self.checkMessage, data=json.dumps(payload), headers=headers)
        self.result = r.json()
        self.assertEqual(r.status_code, 200)
        self.assertEqual(self.result['msg'], 'success')
        self.assertEqual(self.result['code'], '0')

    def test_3_one(self):
        """ 成功添加用户： """
        userName = random_string()  # 用户名
        userPwd = fake.password(length=6, special_chars=False)  # 密码
        trueName = fake.name()  # 真实姓名
        userEmail = fake.company_email()  # 邮箱
        contact = self.g['telphone']  # 手机号
        self.g["userName"] = userName
        self.g["trueName"] = trueName
        self.g["userEmail"] = userEmail
        payload = {'userName': userName, 'userPwd': userPwd, 'trueName': trueName,
                   'contact': contact, 'userEmail': userEmail}
        r = requests.post(self.addUser, data=json.dumps(payload), headers=headers)
        self.result = r.json()
        self.assertEqual(r.status_code, 200)
        self.assertEqual(self.result['msg'], 'success')
        self.assertEqual(self.result['code'], '0')
        print(self.result['data'])

    def test_4_one(self):
        """ 成功提交审核： """
        name = fake.company()  # 企业名称
        companyNumber = get_code()  # 社会信用代码
        phone = self.g['telphone']  # 电话
        fileName = 't.png'  # 图片名称
        fileBase64 = converter(fileName)  # 图片的Base64格式
        companyUsername = self.g["userName"]  # 用户名
        companyEmail = self.g["userEmail"]  # 邮箱
        payload = {'name': name, 'companyNumber': companyNumber, 'phone': phone,
                   'fileName': fileName, 'fileBase64': 'data:image/png;base64,'+str(fileBase64), 'companyUsername': companyUsername,
                   'companyEmail': companyEmail}

        GlobalVar.set_admin(companyUsername,phone)
        r = requests.post(self.coment, data=json.dumps(payload), headers=headers)
        self.result = r.json()
        self.assertEqual(r.status_code, 200)
        self.assertEqual(self.result['msg'], 'success')
        self.assertEqual(self.result['code'], '0')
        print(self.result['data'])


    def test_5_one(self):
        """ 根据手机号获取用户信息 """
        contact = self.g['telphone']  # 手机号
        payload = {'contact': contact}
        r = requests.get(self.getUser, params=payload)
        self.result = r.json()
        self.assertEqual(r.status_code, 200)
        self.assertEqual(self.result['msg'], 'success')
        self.assertEqual(self.result['code'], '0')
        print(self.result['data'])
    # def test_add_event_success(self):
    #     """ 添加成功 """
    #     payload = {'userName': random_string(), 'userPwd': '123456', 'trueName': random_name_str(),
    #                'contact': phoneNO(), 'userEmail': random_emil()}
    #     print(payload)
    #
    #     r = requests.post(self.base_url, data=payload)
    #     print(r)
    #     self.result = r.json()
    #     self.assertEqual(self.result['status'], 200)
    #     self.assertEqual(self.result['message'], 'add event success')


if __name__ == '__main__':
    # test_data.init_data()  # 初始化接口测试数据
    unittest.main()
    # testsuite = unittest.TestSuite()
    # testsuite.addTest(register_admin_test("test_1_one"))
    # testsuite.addTest(register_admin_test("test_2_one"))
    # testsuite.addTest(register_admin_test("test_3_one"))
    # testsuite.addTest(register_admin_test("test_4_one"))
    # testsuite.addTest(register_admin_test("test_4_one"))
    # runner = unittest.TextTestRunner()
    # runner.run(testsuite)
