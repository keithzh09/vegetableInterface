# -*- coding: utf-8 -*-
# @time    : 19-2-28
# @author  : lin

import redis


# redis配置
redis_config = {
    'redis_db': 15,
    # 'redis_host': 'redis',
    'redis_host': '127.0.0.1',
    'redis_port': 6379,
    'redis_password': None
}

# mysql配置
mysql_config = {
    'db_name': 'vegetable_predict',
    'db_user': 'veg_user',
    'db_password': '111222',
    'db_port': 3306,
    'db_host': '106.15.182.134'
}

pool = redis.ConnectionPool(host=redis_config['redis_host'], port=redis_config['redis_port'],
                            db=redis_config['redis_db'])
redis_client = redis.Redis(connection_pool=pool)
