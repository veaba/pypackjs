# todo
from Ruler import Ruler
from rules_inline import StateInline

# rule1
from rules_inline.text import text
from rules_inline.newline import newline
from rules_inline.escape import escape
from rules_inline.backticks import backticks
from rules_inline.strikethrough import strikethrough
from rules_inline.emphasis import emphasisTokenize
from rules_inline.link import link
from rules_inline.image import image
from rules_inline.autolink import autolink
from rules_inline.html_inline import html_inline
from rules_inline.entity import entity

# rule2
from rules_inline.balance_pairs import balance_pairs
from rules_inline.strikethrough import strikethroughPostProcess
from rules_inline.emphasis import emphasisPostProcess
from rules_inline.text_collapse import text_collapse

_rules = [
    ['text', text],
    ['newline', newline],
    ['escape', escape],
    ['backticks', backticks],
    ['strikethrough', strikethrough.tokenize],
    ['emphasis', emphasisTokenize],
    ['link', link],
    ['image', image],
    ['autolink', autolink],
    ['html_inline', html_inline],
    ['entity', entity]
]

_rules2 = [
    ['balance_pairs', balance_pairs],
    ['strikethrough', strikethroughPostProcess],
    ['emphasis', emphasisPostProcess],
    ['text_collapse', text_collapse]
]


class ParserInline:
    def __init__(self):
        self.ruler = Ruler()
        for i in _rules:
            self.ruler.append(_rules[i][0], _rules[i][1])
        self.ruler2 = Ruler()
        for i in _rules:
            self.ruler2.append(_rules2[i][0], _rules2[i][1])

    # todo
    def skipToken(self, state):
        ok = None
        i = None
        pos = state
        rules = self.ruler.getRules('')  # todo
        length = len(rules)
        maxNesting = state.md.options.maxNesting
        cache = state['cache']
        if cache[pos]:
            state['pos'] = cache[pos]
            return
        if state['level'] < maxNesting:
            for i in range(length):
                state['level'] = state['level'] + 1
                ok = rules[i](state, True)
                state['level'] = state['level'] - 1
                if ok:
                    break
        else:
            state['pos']=state['posMax']

    # todo
    def tokenize(self, state):
        ok = None
        i = None
        rules = self.ruler.getRules('')
        length = len(rules)
        end = state.posMax
        maxNesting = state.md.options.maxNesting

        while state['pos'] < end:
            # 尝试所有可能的规则
            # 一旦成功，规则就应该
            # 更新 `state.pos`
            # 更新 `state.tokens`
            # return True
            if state['level'] < maxNesting:
                for i in range(length):
                    ok = rules[i](state, False)
                    if ok:
                        break
            if ok:
                if state['pos'] >= end:
                    break
                continue

            state['pending'] = state['pending'] + state['src'][state['pos'] + 1]

        if state['pending']:
            state.pushPending()

    # todo
    # 推荐令牌
    def parse(self, string, md, env, outTokens):
        state = self.State(string, md, env, outTokens)
        self.tokenize(state)
        rules = self.ruler2.getRules('')
        for i in range(len(rules)):
            rules[i](state)

    # todo
    def State(self, string, md, env, outTokens):
        return StateInline(string, md, env, outTokens)
