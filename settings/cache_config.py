"""
The cache of Session, Token, QuerySet.
"""


class CacheConfig(object):
    # Use redis as cache container.
    REDIS_PORT = 6379

    # Cacheops: Redis Cache, support queryset and get.
    # look:https://github.com/Suor/django-cacheops
    CACHEOPS_REDIS = {
        'host': '127.0.0.1',  # redis-server is on same machine
        'port': REDIS_PORT,        # default redis port
        'db': 2,             # SELECT non-default redis database
                             # using separate redis db or redis instance
                             # is highly recommended
        'socket_timeout': 3,  # Connection timeout
    }
    CACHEOPS_DEFAULTS = {
        # 默认缓存60分钟
        'timeout': 60 * 60
    }
    # PS: 使用cacheops, 实际上就相当于实现了token的cache, 毕竟token存储在DB中
    #     不同于session
    CACHEOPS = {
        # 键值为:app_label:model_name值小写, 其中这个两个值可以通过
        #   obj._meta.app_label, obj._meta.model_name
        # 获取
        'auth.user': {'ops': 'all', 'timeout': 60 * 15},
        'auth.*': {'ops': {'fetch', 'get'}, 'timeout': 60 * 60},
        'auth.permission': {'ops': 'all', 'timeout': 60 * 60},

        # ops: ('get', 'fetch', 'count', 'aggregate', 'exists') == 'all'
        # 使用自动控制: 会与queryset自带缓存混淆, 最好采用手动控制逻辑
        # 唯一好处: 可以对get, count, aggregate进行缓存, fetch本身就具备
        # 更新:
        #   每一次更新之后, 会发现redis缓冲中内容会被清除
        #   任何一个单一原始的更新都会影响redis中的包含该项的filter
        # 忽视更新: 见github文档说明
        'user.person': {'ops': 'all', 'timeout': 60 * 15},
        'user.authtoken': {'ops': ('count', 'fetch'), 'timeout': 60 * 15},
        'user.*': {'ops': 'fetch', 'timeout': 60 * 60},

        '*.*': {},
    }

    CACHEOPS_DEGRADE_ON_FAILURE = True
    # End cacheops

    # Redis Session Cache: https://github.com/martinrusev/django-redis-sessions
    # 前提条件: django已经开启了session支持
    #           见http://python.usyiyi.cn/translate/django_182/topics/http/sessions.html
    #  SESSION_ENGINE = 'redis_sessions.session'
    SESSION_REDIS = {
        'host': '127.0.0.1',
        'port': REDIS_PORT,
        'db': 3,
        'prefix': 'session',
        'socket_timeout': 1
    }
    # End Redis Session Cache
