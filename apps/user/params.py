"""
参数处理
"""


def filter_params(origin, filters):
    """提取有用的参数, 将其他参数丢弃"""
    return {key: origin.get(key) for key in filters if key in origin}


def check_params(origin, filters):
    """检查所有必选的参数是否都在origin中, 如果发现一个不存在, 抛出错误"""
    leak_keys = None
    params = {}
    for key in filters:
        if key in origin:
            params[key] = origin[key]
            continue
        leak_keys = '{}'.format(key)
        break
    if not leak_keys:
        return True, params
    return False, leak_keys
