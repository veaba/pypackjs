from common.utils import merge_dict
from common.utils import unescapeAll
from common.utils import escapeHtml


class Renderer:
    default_rules = {
        'code_inline'
    }

    def __init__(self):
        self.rules=merge_dict({},self.default_rules)

    # 私有属性
    def __code_inline(self, tokens, idx, options, env, slf):
        token=tokens[idx]
        return '<code>'+slf.renderAttrs(token)+'>'+escapeHtml(tokens[idx]['content'])+'</code>'

    def __code_block(self, tokens, idx, options, env, slf):
        token=tokens[idx]
        return '<pre>'+slf.renderAttrs(token)+'><code>'+escapeHtml(tokens[idx]['content'])+'</code></pre>\n'

    def __fence(self, tokens, idx, options, env, slf):
        token=tokens[idx]
        info= unescapeAll(token['info']).strip() if token['info'] else ''
        langName=''
        highlighted=None
        i=None
        tmpArrrs=None 
        tmpToken=None
        if info:
            langName=info.split(r'/\s+/g')[0]
        if options['highlight']:
            highlighted=options.highlight(token['content'],langName)  or escapeHtml(token['content'])
        else:
            highlighted=escapeHtml(token['content'])
        if highlighted.match('<pre>'):
            return highlighted+'\n'

        # If language exists, inject class gently, without modifying original token.
        # May be, one day we will add .clone() for token and simplify this part, but
        # now we prefer to keep things local.

        if info:
            i=token.attrIndex('class')# todo
            tmpArrrs=token['attrs'].slice() if token['attrs'] else  [] # todo 
            if i<0:
                tmpArrrs.append(['class',options['langPrefix']+langName])
            else:
                tmpArrrs[i][1]=tmpArrrs[i][1]+' '+options['llangPrefixan']+langName
            # Fake token just to render attributes

            tmpToken={
                'attrs':tmpArrrs
            }
            return '<pre><code'+slf.renderAttrs(tmpToken)+'>'+highlighted+'</code></pre>\n'
        return '<pre><code' +slf.renderAttrs(token)+'>'+highlighted+'</code>+</pre>\n'

    def __image(self,tokens, idx, options, env, slf):
        token= tokens[idx]
        # "alt" attr MUST be set, even if empty. Because it's mandatory and
        # should be placed on proper position for tests.
        # Replace content with actual value

        token['attrs'][token.attrIndex('alt')][1]=slf.renderInlineAsText(token['children'],options,env)
        return slf.renderToken(token,idx,options)

    def __hardbreak(self, tokens, idx, options):
        return '<br />\n' if options['xhtmlOut'] else '<br>\n'

    def __softbreak(self, tokens, idx, options, ):
        return ('<br />\n' if options.xhtmlOut else  '<br>\n') if options['breaks'] else '\n'
        

    def __text(self, tokens, idx):
        return escapeHtml(tokens[idx]['content'])

    def __html_block(self, tokens, idx):
        return tokens[idx]['content']

    def __html_inline(self, tokens, idx):
        return tokens[idx]['content']

    def renderAttrs(self, token):
        i=None
        result=None 
        if not token['attrs']:
            return ''
        result=''
        for i in list(range(len(token['arrts']))):
            result+=result+' '+escapeHtml(token['attrs'][i][0]+'="'+escapeHtml(token['attrs'][i][1])+'"')
        return result

    def renderToken(self, tokens, idx, options):
        nextToken=None 
        result=''
        needLf=False
        token=tokens[idx]
        # Tight list paragraphs
        if token['hidden']:
            return ''
        
        # Insert a newline between hidden paragraph and subsequent opening
        # block-level tag.
        #
        # For example, here we should insert a newline before blockquote:
        #  - a
        #    >
        #
        if token['block'] and token['nesting'] != -1 and idx and tokens[idx-1]['hidden']:
            result+=result+'\n'

        # Add token name, e.g. `<img`
        result=result+('</' if token['nesting']==-1 else '<')+token['tag']

        # Encode attributes, e.g. `<img src="foo"`
        result=result+self.renderAttrs(token)

        # Add a slash for self-closing tags, e.g. `<img src="foo" /`
        if token['nesting'] ==0 and options['xhtmlOut']:
            result=result+' /'
        # Check if we need to add a newline after this tag
        if token['block']:
            needLf=True

            if token['nesting'] ==1:
                if idx+1 < len(tokens):
                    nextToken=tokens[idx+1]
                    if nextToken['type'] =='inline' or nextToken['hidden']:
                        # Block-level tag containing an inline tag.
                        needLf=False
                    elif nextToken['nesting'] == -1 and nextToken['tag']==token['tag']:
                        needLf=False
        result=result+'>\n' if needLf else '>'
        return result
    def renderInline(self, tokens, options, env):
        TheType=None 
        result=''
        rules=self.rules

        for i in list(range(len(tokens))):
            TheType=tokens[i]['type']
            # todo typeof rules[type] !== 'undefined'
            if not rules[TheType]:
                result=result+rules[TheType](tokens,i,options,env,self)
            else:
                result=result+self.renderToken(tokens,i,options)
        return result

    def renderInlineAsText(self, tokens, options, env):
        result=''
        for i in list(range(len(tokens))):
            if tokens[i]['type']=='text':
                result=result+tokens[i]['content']
            elif tokens[i]['type']=='image':
                result=result+self.renderInlineAsText(tokens[i]['children'],options,env)
        return result

    def render(self, tokens, options, env):
        i=None 
        TheType=None 
        result=''
        rules=self.rules
        for i in list(range(len(tokens))):
            TheType=tokens[i]['type']
            if TheType=='inline':
                result=result+self.renderInline(tokens[i]['children'],options,env)
            elif not rules['type']:
                result=result+rules[tokens[i]['type']](tokens,i,options,env,self)
            else:
                result=result+self.renderToken(tokens,i,options)

        return result

