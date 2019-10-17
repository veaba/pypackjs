# list 转字符
def list_to_str(str_list, code=""):
    if isinstance(str_list, list):
        return code.join(str_list)
    else:
        return ''


# 右边合并左边
# def merge_dict(left, right):
#     print(left,right)
#     return left.update(right)

# 合并两边数组
def merge_dict(left, right):
    return {**left, **right}
