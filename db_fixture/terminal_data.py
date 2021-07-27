import datetime
import json
import sys, time
from datetime import date
from os.path import abspath, dirname

import configparser as cparser

from common.random_common import random_string

sys.path.append('../db_fixture')
try:
    from mysql_db import DB
except ImportError:
    from .mysql_db import DB
# ======== 读取db_config.ini 文件配置 ===========
base_dir = dirname(dirname(abspath(__file__)))
base_dir = base_dir.replace('\\', '/')
file_path = base_dir + "/db_config.ini"

cf = cparser.ConfigParser()

cf.read(file_path)
host = cf.get("terminal_mysqlconf", "host")
port = cf.get("terminal_mysqlconf", "port")
db = cf.get("terminal_mysqlconf", "db_name")
user = cf.get("terminal_mysqlconf", "user")
password = cf.get("terminal_mysqlconf", "password")


# 将测试数据插入表
def init_data():
    mysqldb = DB(host, port, db, user, password)
    # 创建终端数据
    datas = {
        # 终端基础表数据
        'tb_termination_info': [
            {'termination_id': '622456', '`lon_lat`': '112.101536, 40.760664', 'oilConsume': 3343.4,
             'workHours': '453.34', 'creator': 'xueshan'},
        ],
        # 终端任务表数据
        'tb_termination_task': [
            { 'task_id': random_string(), 'termination_id': '622456', 'step': '10','task_lonlat': '112.318859,40.851358', 'status': 0,
             'creator': 'xueshan'},
        ],
    }
    mysqldb.init_data(datas)


# 将历史数据插入表
def init_history_data(task_id, json, status):
    mysqldb = DB(host, port, db, user, password)
    # 创建任务历史数据
    datas = {
        # 终端基础表数据
        'tb_termination_task_history': [
            {'task_id': task_id, '`json`': json, 'status': status},
        ]
    }
    print(json)
    mysqldb.init_data(datas)



def select_data():
    mysqldb = DB(host, port, db, user, password)
    update_sql = 'update tb_termination_task tt, (select b1.id from tb_termination_task b1, (select t.termination_id, max(t.create_time) as time1 from tb_termination_task t where t.status in (0,1) group by t.termination_id having count(*) > 1) b2 where b1.termination_id=b2.termination_id and b1.create_time <> b2.time1) tt1 set tt.status = 3 where tt.id = tt1.id;'
    mysqldb.updateData(update_sql)
    select_sql = 'select a.task_id,a.step,a.task_lonlat,b.termination_id,b.lon_lat,b.oilConsume,b.workHours from tb_termination_task a, tb_termination_info b where a.status =0 and b.termination_id=a.termination_id;'
    results = mysqldb.select(select_sql)
    mysqldb.close()
    # for row in results:
    #     print(type(row))
    return results


def update_termination_data(lon_lat, termination_id, oil, hours, uptime):
    mysqldb = DB(host, port, db, user, password)
    uptime = str(datetime.datetime.strptime(uptime, '%Y%m%d%H%M%S%f'))

    now=str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    update_sql = 'update tb_termination_info set lon_lat=\"' +lon_lat + '\", oilConsume=\"' + str(oil) + '\", workHours=\"' + str(hours) + '\", prompt_time=\"' + uptime + '\", modify_time=\"' +  \
                 now + '\" where termination_id=\"' + str(termination_id) + '\"'
    # update_sql = 'update tb_termination_info set lon_lat=\"' + str(lon_lat) + '\", oilConsume=\"' + str(
    #     oil) + '\", workHours=\"' + str(hours) + '\", prompt_time=\"' + '2021-07-23 10:10:40.40' + '\", modify_time=\"' + \
    #              '2021-07-23 10:10:40.40' + '\" where termination_id=\"' + str(termination_id) + '\"'
    # print(update_sql)
    mysqldb.updateData(update_sql)
    mysqldb.close()


def insert_history_data(task_id, json, status):
    mysqldb = DB(host, port, db, user, password)
    mysqldb.init_history_data(task_id, json, status)
    mysqldb.close()


def update_task_data(task_id, status):
    mysqldb = DB(host, port, db, user, password)
    update_sql = 'update tb_termination_task set status=' + str(status) + ' where task_id=\"' + task_id + '\"'
    print(update_sql)
    mysqldb.updateData(update_sql)
    mysqldb.close()


if __name__ == '__main__':
    init_data()
    # result = select_data()
    # for row in result:
    #     for key in row:
    #         print(key)
    #         print(key + ':' + str(row[key]))
