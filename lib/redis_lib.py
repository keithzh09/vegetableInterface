# coding:UTF-8


from config.db_config import redis_config
import redis

pool = redis.ConnectionPool(host=redis_config['redis_host'], port=redis_config['redis_port'],
                            db=redis_config['redis_db'])
redis_client = redis.Redis(connection_pool=pool)
