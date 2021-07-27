import hashlib
import json
import unittest
import requests
import os, sys
from common.random_common import random_string

from faker import Faker

from interface.common.login import companyLogin
from interface.global_var import global_var_model
from utx import tag, Tag

parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parentdir)
fake = Faker(locale='zh_CN')


# 根据ASCII码的顺序加载测试用例，数字与字母的顺序为：0-9，A-Z，a-z
class test_register_user(unittest.TestCase):
    ''' 企业用户注册 '''

    def setUp(self):
        # 登录
        # self.login = global_var_model.company_login
        # 获取菜单权限
        self.menu = global_var_model.company_menu
        # 添加角色
        self.company_role = global_var_model.company_roleAdd
        # 查找角色
        self.company_roleFind = global_var_model.company_roleFind
        # 添加组织类别
        self.company_Units = global_var_model.company_UnitsAdd
        # 查找单位
        self.company_UnitsFind = global_var_model.company_UnitsFind
        # 添加用户
        self.company_userAdd = global_var_model.company_userAdd
        # 查找企业id
        self.findCompany = global_var_model.findCompany
        # 企业管理员账号
        self.company_admin_userName = global_var_model.company_admin_userName
        self.company_admin_password = global_var_model.company_admin_password
        self.company_admin_phone = global_var_model.company_admin_phone
        self.company_name = global_var_model.company_name
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
        self.g["companyCode"]= self.result['companyCode']
        self.assertEqual(self.result['status_code'], 200)
        self.assertEqual(self.result['msg'], 'success')
        self.assertEqual(self.result['code'], '0')

    @tag(Tag.SMOKE)
    def test_2_one(self):
        """获取菜单权限
           :return:
        """
        if self.g['test_1_one'] != '0':
            result = '{"msg": "test_1_one用例失败"}'
            self.result = json.loads(result)
            self.skipTest("result")
        payload = {"userName": self.company_admin_userName}
        r = requests.post(self.menu, data=json.dumps(payload), headers=self.headers)
        r.encoding = 'utf-8'
        self.result = r.json()
        menu_data = self.result['data']
        menu_code = []
        for i in menu_data:
            menu_code.append(i['menuCode'])
            a = i['children']
            if a:
                for j in range(len(a)):
                    menu_code.append(a[j]['menuCode'])
        self.g["menuList"] = menu_code
        self.assertEqual(r.status_code, 200)
        self.g['test_2_one'] = self.result['code']
        self.assertEqual(self.result['msg'], 'success')
        self.assertEqual(self.result['code'], '0')

    @tag(Tag.SMOKE)
    def test_3_one(self):
        """创建角色
           :return:
        """
        if self.g['test_2_one'] != '0':
            result = '{"msg": "test_2_one用例失败"}'
            self.result = json.loads(result)
            self.skipTest("result")
        roleName = self.company_name + "_" + random_string()
        payload = {"code": "", "userList": [], "roleName": roleName, 'menuList': self.g["menuList"]}
        self.g["roleName"] = roleName
        r = requests.post(self.company_role, data=json.dumps(payload), headers=self.headers)
        r.encoding = 'utf-8'
        self.result = r.json()
        self.g['test_3_one'] = self.result['code']
        self.assertEqual(r.status_code, 200)
        self.assertEqual(self.result['msg'], 'success')
        self.assertEqual(self.result['code'], '0')

    @tag(Tag.SMOKE)
    def test_4_one(self):
        """查找角色
           :return:
        """
        if self.g['test_3_one'] != '0':
            result = '{"msg": "test_3_one用例失败"}'
            self.result = json.loads(result)
            self.skipTest("result")
        payload = {"code": ""}
        r = requests.post(self.company_roleFind, data=json.dumps(payload), headers=self.headers)
        r.encoding = 'utf-8'
        self.result = r.json()
        data = self.result['data']
        for i in data:
            if i['roleName'] == self.g["roleName"]:
                self.g["roleId"] = i['roleId']
                break
        self.g['test_4_one'] = self.result['code']
        self.assertEqual(r.status_code, 200)
        self.assertEqual(self.result['msg'], 'success')
        self.assertEqual(self.result['code'], '0')

    @tag(Tag.SMOKE)
    def test_5_one(self):
        """创建单位
           :return:
        """
        if self.g['test_1_one'] != '0':
            result = '{"msg": "test_1_one用例失败"}'
            self.result = json.loads(result)
            self.skipTest("result")
        constructUnitsName = self.company_name + "_" + random_string()
        unitsType = self.company_name + "_" + random_string()
        self.g['constructUnitsName'] = constructUnitsName
        self.g['unitsType'] = unitsType
        payload = {"constructUnitsName": constructUnitsName, "unitsType": unitsType, "userList": []}
        r = requests.post(self.company_Units, data=json.dumps(payload), headers=self.headers)
        r.encoding = 'utf-8'
        self.result = r.json()
        self.g['test_5_one'] = self.result['code']
        self.assertEqual(r.status_code, 200)
        self.assertEqual(self.result['msg'], 'success')
        self.assertEqual(self.result['code'], '0')

    @tag(Tag.SMOKE)
    def test_6_one(self):
        """查找单位
           :return:
        """
        if self.g['test_4_one'] != '0':
            result = '{"msg": "test_5_one用例失败"}'
            self.result = json.loads(result)
            self.skipTest("result")
        payload = {"companyCode": self.g["companyCode"], "constructUnitsName": ""}
        r = requests.post(self.company_UnitsFind, data=json.dumps(payload), headers=self.headers)
        r.encoding = 'utf-8'
        self.result = r.json()
        data = self.result['data']
        for i in data:
            if i['unitsType'] == self.g["unitsType"]:
                children = i['children']
                for j in children:
                    if j['constructUnitsName'] == self.g["constructUnitsName"]:
                        self.g['unitsCode'] = j['unitsCode']
                        break
        self.g['test_6_one'] = self.result['code']
        self.assertEqual(r.status_code, 200)
        self.assertEqual(self.result['msg'], 'success')
        self.assertEqual(self.result['code'], '0')

    @tag(Tag.SMOKE)
    def test_7_one(self):
        """创建用户
           :return:
        """
        if self.g['test_4_one'] != '0' or self.g['test_6_one'] != '0':
            result = '{"msg": "test_4_one用例失败|test_6_one用例失败"}'
            self.result = json.loads(result)
            self.skipTest("result")
        trueName = fake.name()  # 真实姓名
        userName = random_string()  # 用户名
        userPwd = fake.password(length=6, special_chars=False)  # 密码
        post = "职位"
        telphone = fake.phone_number()  # 手机号
        email = fake.company_email()  # 邮箱
        unitsCode = self.g['unitsCode']
        roleId = self.g['roleId']
        print('---用户信息------')
        print(userName)
        print(userPwd)
        print(telphone)
        payload = {"trueName": trueName, "userName": userName, "userPwd": hashlib.md5(userPwd.encode()).hexdigest(),
                   "unitsCode": unitsCode, "post": post, "telephone": telphone,
                   "roleId": roleId, "email": email, "status": 1}
        r = requests.post(self.company_userAdd, data=json.dumps(payload), headers=self.headers)
        r.encoding = 'utf-8'
        self.result = r.json()
        self.assertEqual(r.status_code, 200)
        self.assertEqual(self.result['msg'], 'success')
        self.assertEqual(self.result['code'], '0')


if __name__ == '__main__':
    unittest.main()
