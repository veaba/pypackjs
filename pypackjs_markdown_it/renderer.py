from common.utils import merge_dict
from common.utils import unescapeAll
from common.utils import escapeHtml


class Renderer:
    default_rules = {
        'code_inline'
    }

    def __init__(self):
        pass

    # 私有属性
    def __code_inline(self, tokens, idx, options, env, slf):
        pass

    def __code_block(self, token, idx, options, env, slf):
        pass

    def __fence(self, tokens, idx, options, env, slf):
        pass

    def __image(tokens, idx, options, env, slf):
        pass

    def __hardbreak(self, tokens, idx, options):
        pass

    def __softbreak(self, tokens, idx, options, ):
        pass

    def __text(self, tokens, idx):
        pass

    def __html_block(self, tokens, idx):
        pass

    def __html_inline(self, tokens, idx):
        pass

    def renderAttrs(self, token):
        pass

    def renderToken(self, tokens, idx, options):
        pass

    def renderInline(self, tokens, options, env):
        pass

    def renderInlineAsText(self, tokens, options, env):
        pass

    def render(self, tokens, options, env):
        pass
