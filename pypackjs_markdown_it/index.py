# python 版本markdown-it pymarkdown-it
from common.utils import isString, throwError, assign_dict, isArray
from parser_inline import ParserInline
from parser_block import ParserBlock
from parser_core import ParserCore
from renderer import Renderer
import re


# @staticmethod
# @classmethod
class MarkdownIt:
    def __init__(self, presetName, options):
        self.presetName = presetName
        self.options = options
        self.inline = ParserInline()  # todo
        self.block = ParserBlock()  # todo
        self.core = ParserCore()  # todo
        self.renderer = Renderer()  # todo
        # todo self.linkify= LinkifyIt() 底层的URL解析工具，暂停拓展开发

        # 设置私有属性
        from presets.default import default
        from presets.zero import zero
        from presets.commonmark import commonmark
        self.__config = {
            'default': default,
            'zero': zero,
            'commonmark': commonmark
        }
        self.__BAD_PROTO_RE = re.compile(r'/^(vbscript|javascript|file|data):/')
        self.GOOD_DATA_RE = re.compile(r'/^data:image\/(gif|png|jpeg|webp);/')
        MarkdownIt.init(self)

    # 静态方法
    # @classmethod 入参是类本身
    @staticmethod
    def init(self):
        if not isinstance(self, MarkdownIt):
            return MarkdownIt(self.presetName, self.options)
        if not self.options:
            if not isString(self.presetName):
                self.options = self.presetName or {}
                self.presetName = 'default'

    def __set(self, options):
        if options is None:
            options = {}
        assign_dict(self.options, options)
        return self

    def configure(self, presets):
        # 先判断不存在
        if not presets:
            return throwError('不存在：presets')
        if isString(presets):
            self.presetName = presets
            presets = self.__config[self.presetName]  # TODO 这里能重写上面这个变量吗？

    # todo 链式调用
    def enable(self, array, ignoreInvalid):
        result = []
        if not isArray(array):
            array = [array]

        for item in ['core', 'block', 'inline']:
            # todo
            result.extend(self[item]['ruler'].enable(array, True))
        # todo class 如何循环声明？
        result.extend(self['line']['ruler2'].enable(array, True))

        missed = [item for item in array if item in result]
        if len(missed) and not ignoreInvalid:
            return throwError('MarkdownIt. Failed to enable unknown rule(s): ')
        return self

    # todo 禁用规则
    def disabled(self, array, ignoreInvalid):
        result = []
        if not isArray(array):
            array = [array]
        for item in ['core', 'block', 'inline']:
            # todo
            result.extend(self[item]['ruler'].disabled(array, True))
            # todo class 如何循环声明？
        result.extend(self['line']['ruler2'].disabled(array, True))

        missed = [item for item in array if item in result]
        if len(missed) and not ignoreInvalid:
            return throwError('MarkdownIt. Failed to disable unknown rule(s): ')
        return self

    # todo 链式
    # markdownIt.use(plugin,params),params 是多个参数
    #
    def use(self, plugin, *params):
        args = [self] + params
        plugin(args)
        return self

    # todo 内部解析
    def parse(self, src, env):
        if not isString(src):
            return throwError('Input data should be a String')
        state = self.core.State(src, self, env)
        self.core.process(state)
        return state['tokens']

    # todo render
    def render(self, src, env):
        env = env or {}
        return self.renderer.render(self.parse(src, env), self.options, env)

    # todo 解析行数据
    def parseInline(self, src, env):
        state = self.core.State(src, self, env)
        print(state)  # todo
        state['inlineMode'] = True
        self.core.process(state)
        return state['tokens']

    # renderInline
    def renderInline(self, src, env):
        env = env or {}
        return self.renderer.render(self.parseInline(src, env), self.options, env)


markdown = MarkdownIt('aa', {"name": "ok"})
