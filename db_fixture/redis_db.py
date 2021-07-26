import random
import string
from os.path import dirname, abspath


import configparser as cparser


import redis
# ======== 读取db_config.ini 文件配置 ===========
base_dir = dirname(dirname(abspath(__file__)))
base_dir = base_dir.replace('\\', '/')
file_path = base_dir + "/db_config.ini"

cf = cparser.ConfigParser()

cf.read(file_path)
host = cf.get("redis_conf", "host")
port = cf.get("redis_conf", "port")
db = cf.get("redis_conf", "db_name")
password = cf.get("redis_conf", "password")

class Redis:
    def __init__(self):
        try:
            # 使用连接池连接数据库。这样就可以实现多个Redis实例共享一个连接池
            pool = redis.ConnectionPool(host=host, port=port,
                                        password=password)
            self.r = redis.Redis(connection_pool=pool, db=db)

        except redis.exceptions as e:
            print("redis Error %d: %s" % (e.args[0], e.args[1]))

    # 获取手机验证码
    def registerIDcode(self, phone):
        name='company_register' + phone
        code=self.r.get(name)
        if not code:
            random_code= "".join(random.sample([x for x in  string.digits], 6))
            self.r.set(name, random_code)
            return random_code
        else:
            b = bytes.decode(self.r.get(name))
            return b

    # 关闭redis连接
    def close(self):
        self.r.connection_pool.disconnect()
