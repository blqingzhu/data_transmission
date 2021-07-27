import hashlib
import json
import unittest
import requests
import os, sys

from common.CreditIdentifie import get_code
from db_fixture.redis_db import Redis
from common.random_common import random_string, converter

from faker import Faker

from interface.global_var import global_var_model
from utx import tag, Tag

# 企业管理员账号
admin_userName = global_var_model.admin_userName
admin_password = global_var_model.admin_password  # 管理后台密码
login = global_var_model.login
# 企业管理员账号
company_loginUrl = global_var_model.company_login


# 管理后台登录
def admin_login(admin_headers):
    payload = {'userName': admin_userName, 'password': hashlib.md5(admin_password.encode()).hexdigest()}
    r = requests.post(login, data=json.dumps(payload), headers=admin_headers)
    r.encoding = 'utf-8'
    result = r.json()
    data = result['data']
    code = result['code']
    uid = data['uid']
    admin_headers['Cookie'] = 'Admin-Token=' + uid
    admin_headers['uid'] = uid
    retult = {"code": code, "admin_headers": admin_headers, "status_code": r.status_code, "msg": result['msg']}
    return retult


# 服务后台登录
def companyLogin(company_userName, company_password, headers):
    """登录
        :return:
    """
    payload = {'name': company_userName,
               'passwd': hashlib.md5(company_password.encode()).hexdigest()}

    r = requests.post(company_loginUrl, data=json.dumps(payload), headers=headers)
    r.encoding = 'utf-8'
    result = r.json()
    data = result['data']
    code = result['code']
    uid = data['uid']
    companyCode = data['companyCode']
    userSign = data['userSign']
    roleType = data['roleType']
    headers[
        'Cookie'] = 'Admin-Token=%s;  roleType=%s; companyCode=%s; uid=%s; userSign=%s' % (
        uid, roleType, companyCode, uid, userSign)
    headers['roleType'] = str(roleType)
    headers['companyCode'] = companyCode
    headers['uid'] = uid
    result = {"code": code, "headers": headers, "status_code": r.status_code, "msg": result['msg'],'companyCode':companyCode}
    return result
