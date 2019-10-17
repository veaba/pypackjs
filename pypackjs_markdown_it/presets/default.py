# markdown-it default option
default = {
    'options': {
        'html': False,  # 启用HTML标签
        'xhtmlOut': False,  # 使用“/”关闭单个标记（<br/>）
        'breaks': False,  # 将段落中的\n转换为<br>
        'langPrefix': 'language-',  # language的css语言前缀
        'linkify': False,  # TODO 暂停这项目，自动将类似url的文本转换到链接

        # 启用某些语言中性替换+引号美化
        'typographer': False,
        # 双引号+单引号替换对，启用排版器时，
        'quotes': '\u201c\u201d\u2018\u2019',  # “”‘’
        # 高亮function
        'hightlight': None,
        'maxNesting': 100  # 内部保护，回归极限
    },
    'components': {
        'core': {},
        'block': {},
        'inline': {}
    }
}
