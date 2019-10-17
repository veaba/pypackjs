# 判断是否是字符串
def isString(string):
    return isinstance(string, str)


def throwError(msg):
    raise RuntimeError('!error：'+msg)

# 合并两边数组
def merge_dict(left, right):
    return {**left, **right}
