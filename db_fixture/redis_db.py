print("=====================redis数据库=====================")

import redis


class Redis:
    def __init__(self, host, port, db):
        try:
            # 使用连接池连接数据库。这样就可以实现多个Redis实例共享一个连接池
            pool = redis.ConnectionPool(host=host, port=port,
                                        password=password)
            r = redis.Redis(connection_pool=pool, db=db)
        except redis.exceptions as e:
            print("redis Error %d: %s" % (e.args[0], e.args[1]))

    def registerIDcode(self, phone):
        b = bytes.decode(self.r.get('company_register' + phone))
        return b

    # 关闭redis连接
    def close(self):
        self.r.connection_pool.disconnect()