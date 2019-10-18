# todo
from rules import Rules


class ParserInline:
    def __init__(self):
        self.ruler = Rules()
        pass

    # todo
    def skipToken(self, state):
        ok = None
        i = None
        pos = state
        rules = self.ruler.getRules('')  # todo
        length = len(rules)
        maxNesting = state.md.options.maxNesting
        cache = state['cache']

    # todo
    def tokenize(self):
        pass

    # todo
    def State(self):
        pass
