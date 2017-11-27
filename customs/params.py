"""
参数处理: 参数过滤, 参数检查
"""


def filter_params(origin, filters):
    return {key: origin.get(key) for key in filters if key in origin}


def check_params(origin, filters):
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
