from rules_core.normalize import normalize
from rules_core.block import block
from rules_core.inline import inline
from rules_core.replacements import replacements
from rules_core.smartquotes import smartquotes
from ruler import Ruler
from rules_core.state_core import StateCore

_rules = [
    ['normalize', normalize],
    ['block', block],
    ['inline', inline],
    ['replacements', replacements],
    ['smartquotes', smartquotes],
]


class Core:
    def __init__(self):
        self.ruler = Ruler()
        for i in range(len(_rules)):
            self.ruler.append(_rules[i][0], _rules[i][1])

    def process(self, state):
        rules = self.ruler.getRules('')
        for i in range(len(rules)):
            rules[i](state)

    @property
    def State(self):
        return StateCore
