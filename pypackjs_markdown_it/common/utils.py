# 判断是否是字符串
def isString(string):
    return isinstance(string, str)


# 判断是不是数组/list
def isList(array):
    return isinstance(array, list)


# 判断数组的别称
def isArray(array):
    return isinstance(array, list)


# 抛出错误异常，中断程序
def throwError(msg):
    raise RuntimeError('!error：' + msg)


# 合并两边数组
def merge_dict(left, right):
    return {**left, **right}


# 右边字典合并到左边字典
def assign_dict(left, right):
    left.update(right)

def unescapeAll(string):
    pass

def escapeHtml(string):
    pass

# 判断是不是空白行
def isWhiteSpace(code):
    if 0x2000 < code <= 0x200A:
        return True
    # 这种写法来接近switch/case 语法，python 无switch/case
    true_map = {
        '0x09': True,  # \t
        '0x0A': True,  # \n
        '0x0B': True,  # \v
        '0x0C': True,  # \f
        '0x0D': True,  # \r
        '0x0E': True,
        '0x20': True,
        '0xA0': True,
        '0x1680': True,
        '0x202F': True,
        '0x205F': True,
        '0x3000': True,
    }

    if not true_map[code]:
        return False
    return true_map[code]


# todo 目前没有星体角色支持。
# def isPunctChar():
#     return UNICODE_PUNCT_RE


# 不要与Unicode标点混淆！！！它缺少ascii范围内的一些字符。
def isMdAsciiPunct(ch):
    ascii_list = [
        0x21,  # !
        0x22,  # "
        0x23,  # #
        0x24,  # $
        0x25,  # %
        0x26,  # &
        0x27,  # '
        0x28,  # (
        0x29,  # )
        0x2A,  # *
        0x2B,  # +
        0x2C,  # ,
        0x2D,  # -
        0x2E,  # .
        0x2F,  # /
        0x3A,  # :
        0x3B,  # ;
        0x3C,  # <
        0x3D,  # =
        0x3E,  # >
        0x3F,  # ?
        0x40,  # @
        0x5B,  # [
        0x5C,  # \
        0x5D,  # ]
        0x5F,  # ^
        0x60,  # `
        0x7B,  # {
        0x7C,  # |
        0x7D,  # }
        0x7E  # ~
    ]

    if ch in ascii_list:
        return True
    else:
        return False


