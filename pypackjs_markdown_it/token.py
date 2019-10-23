# new Token(type, tag, nesting)
# 创建新令牌并填充传递的属性。
# TODO 后续如何处理关键字type呢？


class Token:
    def __init__(self, type, tag, nesting):
        #  Token#type -> String
        # Type of the token (string, e.g. "paragraph_open")
        self.type = type

        #  Token#tag -> String
        # html tag name, e.g. "p"
        self.tag = tag

        # Token#attrs -> Array
        # Html attributes. Format: `[ [ name1, value1 ], [ name2, value2 ] ]`
        self.attrs = None

        # Token#map -> Array
        # Source map info. Format: `[ line_begin, line_end ]`
        self.map = None

        # Token#nesting -> Number
        # Level change (number in {-1, 0, 1} set), where:
        # `1` means the tag is opening
        # `0` means the tag is self-closing
        # `-1` means the tag is closing
        self.nesting = nesting

        # Token#level -> Number
        # nesting level, the same as `state.level`
        self.level = 0

        # Token#children -> Array
        # An array of child nodes (inline and img tokens)
        self.children = None

        # Token#content -> String
        # In a case of self-closing tag (code, html, fence, etc.),
        # it has contents of this tag.
        self.content = ''

        # Token#markup -> String
        # '*' or '_' for emphasis, fence string for fence, etc.
        self.markup = ''

        # Token#info -> String
        # fence infostring
        self.info = ''

        # Token#meta -> Object
        # A place for plugins to store an arbitrary data
        self.meta = None

        # Token#block -> Boolean
        # True for block-level tokens, false for inline tokens.
        # Used in renderer to calculate line breaks
        self.block = False

        # Token#hidden -> Boolean
        # If it's true, ignore this element when rendering. Used for tight lists
        # to hide paragraphs.
        self.hidden = False

    # Token.attrIndex(name) -> Number
    # Search attribute index by name.
    def attrIndex(self, name):
        if not self.attrs:
            return -1
        attrs = self.attrs
        for i in range(len(attrs)):
            if attrs[i][0] == name:
                return i

        return -1

    # Token.attrPush(attrData)
    #  Add `[ name, value ]` attribute to list. Init attrs if necessary
    def attrPush(self, attrData):
        if self.attrs:
            self.attrs.append(attrData)
        else:
            self.attrs = [attrData]

    # Token.attrSet(name, value)
    # Set `name` attribute to `value`. Override old value if exists.
    def attrSet(self, name, value):
        idx = self.attrIndex(name)
        attrData = [name, value]
        if idx < 0:
            self.attrPush(attrData)
        else:
            self.attrs[idx] = attrData

    # Token.attrGet(name)
    # Get the value of attribute `name`, or null if it does not exist.
    def attrGet(self, name):
        idx = self.attrIndex(name)
        value = None
        if idx > 0:
            value = self.attrs[idx][1]
        return value

    # Token.attrJoin(name, value)
    # Join value to existing attribute via space. Or create new attribute if not
    # exists. Useful to operate with token classes.
    def attrJoin(self, name, value):
        idx = self.attrIndex(name)
        if idx < 0:
            self.attrPush([name, value])
        else:
            self.attrs[idx][1] = self.attrs[idx][1] + ' ' + value
