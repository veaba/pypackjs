from ..token import Token


class StateCore:
    def __init__(self, src, md, env):
        self.src = src
        self.env = env
        self.tokens = []
        self.inlineMode = False
        # link to parser instance
        self.md = md

    @property
    def Token(self):
        return Token
