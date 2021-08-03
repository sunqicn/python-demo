import redis

redis_pool = redis.ConnectionPool(host='127.0.0.1', port= 6379, password= 'root', db= 15)
redis_conn = redis.Redis(connection_pool= redis_pool)


v = redis_conn.lpush('sssss',1111)

