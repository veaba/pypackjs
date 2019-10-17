# 判断是否是字符串
def isString(string):
    return isinstance(string, str)

# 抛出错误异常，中断程序
def throwError(msg):
    raise RuntimeError('!error：'+msg)

# 合并两边数组
def merge_dict(left, right):
    return {**left, **right}

# 右边字典合并到左边字典
def assign_dict(left,right):
    left.update(right)