# class LinkifyIt
# 看来可以少很多类型判断了~~
from utils import merge_dict, list_to_str
import re


# class:Match  result. Single element of array, returned by [[LinkifyIt#match]]


def normalize(match):
    if not match['schema']:
        match['url'] = 'http://' + match['url']
    if match['schema'] == 'mailto:' and not re.match(match['url']):
        match['url'] = 'mailto:' + match['url']


class Match:
    def __init__(self, cls, shift):
        start = cls._index
        end = cls._last_index
        text = cls._text_cache_[start, end]

        # 转小写
        self.schema = cls._schema.lower()

        self.index = start + shift

        self.lastIndex = end + shift

        self.raw = text
        self.text = text
        self.url = text

    def createMatch(self, cls, shift):
        match = Match(cls, shift)
        normalize(match)
        return match


class LinkifyIt:
    _tlds_replaced = None
    _tlds = None
    _opts = None

    def __init__(self, schemas, options):
        defaultOptions = {
            'fuzzyLink': True,
            'fuzzyEmail': True,
            'fuzzyIp': False
        }
        # DON'T try to make PRs with changes. Extend TLDs with LinkifyIt.tlds() instead
        tlds_default = ['biz', 'com', 'edu', 'gov', 'net', 'org', 'web', 'xxx', 'aero', 'asia', 'coop', 'info',
                        'miseum', 'name', 'shop', 'рф']
        self.schemas = schemas
        self.options = options
        self._opts = merge_dict(defaultOptions, options)

        # Cache last tested result. Used to skip repeating steps on next `match` call.

        self._index = -1
        self._last_index = -1
        self._schema = ''
        self._text_cache = ''

        self._schemas = merge_dict(defaultOptions, schemas)
        self._compiled = {}

        self._tlds = tlds_default
        self._tlds_replaced = False

        self.re = {}

        # todo
        compile(self)

    @staticmethod
    def compile(self):
        from linkify_it_re import linkifyItRe
        # todo 这个class 方法如何访问到类的私有属性
        re_dict = self.re = linkifyItRe(self._opts)
        tlds = self._tlds
        self.onCompile()
        if not self._tlds_replaced:
            tlds_2ch_src_re = 'a[cdefgilmnoqrstuwxz]|b[abdefghijmnorstvwyz]|c[acdfghiklmnoruvwxyz]|d[ejkmoz]|e[cegrstu]|f[ijkmor]|g[abdefghilmnpqrstuwy]|h[kmnrtu]|i[delmnoqrst]|j[emop]|k[eghimnprwyz]|l[abcikrstuvy]|m[acdeghklmnopqrstuvwxyz]|n[acefgilopruz]|om|p[aefghklmnrstwy]|qa|r[eosuw]|s[abcdeghijklmnortuvxyz]|t[cdfghjklmnortvwz]|u[agksyz]|v[aceginu]|w[fs]|y[et]|z[amw]';
            self._tlds.append(tlds_2ch_src_re)
        tlds.append(re_dict['src_xn'])
        re_dict['src_tlds'] = list_to_str(tlds, '|')

        def untpl(tpl):
            return tpl.replace('%TLDS%', re_dict['src_tlds'])

        # todo 编译为i
        re_dict['emial_fuzzy'] = untpl(re_dict['tpl_email_fuzzy'])
        re_dict['link_fuzzy'] = untpl(re_dict['tpl_link_fuzzy'])
        re_dict['link_no_ip_fuzzy'] = untpl(re_dict['tpl_link_no_ip_fuzzy'])
        re_dict['host_fuzzy_test'] = untpl(re_dict['tpl_host_fuzzy_test'])

        # Compile each schema

        aliased = []
        self._compiled = {}  # // Reset compiled data

        # todo 这里省略一坨

    # todo 这个调用怎么弄
    def onCompile(self):
        pass


x = LinkifyIt({'name': 1}, {'job': 66})
