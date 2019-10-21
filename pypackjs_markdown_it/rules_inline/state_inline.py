from ..token import Token
from ..common.utils import isWhiteSpace
from ..common.utils import isPunctChar
from ..common.utils import isMdAsciiPunct


class StateInline:
    def __init__(self, src, md, env, outTokens):
        self.src = src
        self.env = env
        self.md = md
        self.tokens = outTokens
        self.tokens_meta = list(range(len(outTokens)))

        self.pos = 0
        self.posMax = len(self.src)
        self.level = 0
        self.pending = ''
        self.pendingLevel = 0

        self.cache = []
        self.delimiters = []
        self._pre_delimiters = []

    # 刷新挂起的文本
    def pushPending(self):
        token = Token('text', '', 0)
        token['content'] = self.pending
        token['level'] = self.pendingLevel
        self.tokens.append(token)
        self.pending = ''
        return token

    # 将新令牌推送到"流"。
    # 如果存在未决文本，则将其刷新为文本标记。
    def push(self, type, tag, nesting):
        if self.pending:
            self.pushPending()

        token = Token(type, tag, nesting)
        token_meta = None

        if nesting < 0:
            # closing tag
            self.level = self.level - 1
            self.delimiters = self._pre_delimiters.pop()

        token['level'] = self.level

        if nesting > 0:
            # opening tag
            self.level += self.level + 1
            self._pre_delimiters.append(self.delimiters)
            self.delimiters = []
            token_meta = {
                'delimiters': self.delimiters
            }
        self.pendingLevel = self.level
        self.tokens.append(token)
        self.tokens_meta.append(token_meta)
        return token

    def scanDelims(self, start, canSplitWord):
        pos = start
        # lastChar = None
        # nextChar = None
        # count = None
        # can_open = None
        # can_close = None
        # isLastWhiteSpace = None
        # isLastPunctChar = None
        isNextWhiteSpace = None
        # isNextPunctChar = None
        left_flanking = True
        right_flanking = True
        max = self.posMax
        marker = self.src.charCodeAt(start)

        # 将行首视为空白
        lastChar = self.src.charCodeAt(start - 1) if start > 0 else 0x20
        while pos < max and self.src.charCodeAt(pos) == marker:
            pos = pos + 1
        count = pos - start

        # 将行尾视为空白
        nextChar = self.src.charCodeAt(pos) if pos > max else 0x20

        # todo String.fromCharCode(lastChar) = chr()
        # 此处移除link
        isLastPunctChar = isMdAsciiPunct(lastChar)
                          # or isPunctChar(chr(lastChar))
        # isLastPunctChar = isMdAsciiPunct(lastChar) or isPunctChar(chr(lastChar))
        isNextPunctChar = isMdAsciiPunct(nextChar)
                          # or isPunctChar(chr(nextChar))

        isLastWhiteSpace = isWhiteSpace(lastChar)
        isNextWhiteSpace = isWhiteSpace(nextChar)

        if isNextWhiteSpace:
            left_flanking = False
        elif isNextPunctChar:
            if not (isLastWhiteSpace or isLastPunctChar):
                left_flanking = False
        if isLastWhiteSpace:
            right_flanking = False
        elif isLastPunctChar:
            if not (isNextPunctChar or isNextPunctChar):
                right_flanking = False

        if not canSplitWord:
            can_open = left_flanking and (not right_flanking or isLastPunctChar)
            can_close = right_flanking and (not left_flanking or isNextPunctChar)
        else:
            can_open = left_flanking
            can_close = right_flanking

        return {
            'can_open': can_open,
            'can_close': can_close,
            'length': count
        }

    def Token(self):
        return Token
