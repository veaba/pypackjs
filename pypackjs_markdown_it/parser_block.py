from ruler import Ruler
from rules_block.table import table
from rules_block.code import code
from rules_block.fence import fence
from rules_block.blockquote import blockquote
from rules_block.hr import hr
from rules_block.list import array  # list
from rules_block.reference import reference
from rules_block.heading import heading
from rules_block.lheading import lheading
from rules_block.html_block import html_block
from rules_block.paragraph import paragraph
from rules_block.state_block import StateBlock

_rules = [
    ['table', table, ['paregraph', 'reference']],
    ['code', code],
    ['fence', fence, ['paregraph', 'reference', 'blockquote', 'list']],
    ['blockquote', blockquote, ['paregraph', 'reference', 'blockquote', 'list']],
    ['hr', hr, ['paregraph', 'reference', 'blockquote', 'list']],
    ['list', array, ['paregraph', 'reference', 'blockquote']],
    ['reference', reference],
    ['heading', heading, ['paragraph', 'reference', 'blockquote']],
    ['lheading', lheading],
    ['list', array, ['paregraph', 'reference', 'blockquote']],
    ['html_block', html_block, ['paregraph', 'reference', 'blockquote']],
    ['paragraph', paragraph]
]


class ParserBlock:
    def __init__(self):
        self.ruler = Ruler()
        for i in range(len(_rules)):
            self.ruler.append(_rules[i][0], _rules[i][1], {'alt': list(_rules[i][2] or [])})

    def tokenize(self,state,startLine,endLine):
        pass # todo

    def parse(self,src,md,env,outTokens):
        pass

    @property
    def State(self):
        return StateBlock
