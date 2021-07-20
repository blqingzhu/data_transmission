# coding=utf8
import pymysql.cursors
from os.path import abspath, dirname
import configparser as cparser

# ======== 读取db_config.ini 文件配置 ===========
base_dir = dirname(dirname(abspath(__file__)))
base_dir = base_dir.replace('\\', '/')
file_path = base_dir + "/db_config.ini"

cf = cparser.ConfigParser()

cf.read(file_path)
host = cf.get("mysqlconf", "host")
port = cf.get("mysqlconf", "port")
db = cf.get("mysqlconf", "db_name")
user = cf.get("mysqlconf", "user")
password = cf.get("mysqlconf", "password")


# ======== 封装M有ySQL基本操作 ===================
class DB:

    def __init__(self):
        try:
            # 连接数据库
            self.connection = pymysql.connect(host=host,
                                              port=int(port),
                                              user=user,
                                              password=password,
                                              db=db,
                                              charset='utf8mb4',
                                              cursorclass=pymysql.cursors.DictCursor)
        except pymysql.err.OperationalError as e:
            print("Mysql Error %d: %s" % (e.args[0], e.args[1]))

    # 清除表数据
    def clear(self, table_name):
        # real_sql = "truncate table " + table_name + ";"
        real_sql = "delete from " + table_name + ";"
        with self.connection.cursor() as cursor:
            cursor.execute("SET FOREIGN_KEY_CHECKS=0;")
            cursor.execute(real_sql)
        self.connection.commit()

    # 插入表数据
    def insert(self, table_name, table_data):
        for key in table_data:
            table_data[key] = "'" + str(table_data[key]) + "'"
        key = ','.join(table_data.keys())
        value = ','.join(table_data.values())
        real_sql = "INSERT INTO " + table_name + " (" + key + ") VALUES (" + value + ")"
        # print(real_sql)

        with self.connection.cursor() as cursor:
            cursor.execute(real_sql)

        self.connection.commit()

    # 更新表数据
    def updateData(self, table_name, dateID, datekey, data):
        """
        更新数据库数据
        :param datekey: 主键名
        :param table_name:表名
        :param dateID: 主键值
        :param data: 需要修改成的数据json格式
        :return:
        """
        # table = self._toChar(table_name)
        # date = self._toStr(dateID)
        for key in data:
            data[key] = "'" + str(data[key]) + "'"
        string = []
        for k, v in data.items():
            string.append(k + '=' + str(v) + '')
        update_str = ','.join(string)
        if not self._hasThisId(table_name, dateID, datekey):
            # 如果没有这个主键值，那还改个屁，直接返回
            return
        # 同样也是将data这个numpy数组转换一下成二进制流数据
        b_data = data.tostring()
        sql = "update " + table_name + " set  %s where %s = %s;"
        self.cur.execute(sql, (b_data, datekey, update_str))
        self.database.commit()
        print("已更新数据：%s..." % dateID)

    def _hasThisTable(self, table_name):
        """
        判断是否存在此表
        :param table_name:表名
        :return: True  or  False
        """
        sql = "show tables;"
        self.cur.execute(sql)
        results = self.cur.fetchall()
        for r in results:
            if r[0] == table_name:
                return True
        else:
            return False

    def _hasThisId(self, table_name, dateID, datekey):
        """
        判断在此表中是否已经有此主键
        :param datekey: 主键名
        :param table_name: 表名
        :param dateID: 主键值
        :return: True  or  False
        """
        sql = "select " + datekey + " from " + table_name + ";"
        self.cur.execute(sql)
        ids = self.cur.fetchall()
        for i in ids:
            if i[0] == dateID:
                return True
        else:
            return False

    def _toChar(self, string):
        """
        为输入的字符串添加一对反引号，用于表名、字段名等对关键字的规避
        :param string:
        :return:
        """
        return "`%s`" % string

    def _toStr(self, string):
        '''
        为输入的字符串添加一对单引号，用于数值处理，规避字符串拼接后原字符串暴露问题
        :param string:
        :return:
        '''
        return "'%s'" % string

    # 关闭数据库连接
    def close(self):
        self.connection.close()

    # 插入表数据
    def init_data(self, datas):
        for table, data in datas.items():
            self.clear(table)
            for d in data:
                self.insert(table, d)
        self.close()


if __name__ == '__main__':
    db = DB()
    table_name = "sign_event"
    data = {'id': 1, 'name': '红米', '`limit`': 2000, 'status': 1, 'address': '北京会展中心',
            'start_time': '2016-08-20 00:25:42'}
    table_name2 = "sign_guest"
    data2 = {'realname': 'alen', 'phone': 12312341234, 'email': 'alen@mail.com', 'sign': 0, 'event_id': 1}

    db.clear(table_name)
    db.insert(table_name, data)
    db.close()
