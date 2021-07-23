print("=====================redis数据库=====================")

import redis

# 使用连接池连接数据库。这样就可以实现多个Redis实例共享一个连接池
pool = redis.ConnectionPool(host='r-m5el1rv4i4t6k47cghpd.redis.rds.aliyuncs.com', port=6379,
                            password='FvWO2WqoKbyfS3ji')
r = redis.Redis(connection_pool=pool, db=0)
b = bytes.decode(r.get('12345678'))
print(b)
