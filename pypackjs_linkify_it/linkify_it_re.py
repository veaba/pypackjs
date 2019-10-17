# 如何import 上一个目录的文件
from plugins.pypackjs_ucMicro import Any, Cc, Cf, P, Z


def linkifyItRe(opts):
    re_obj = {
        'src_Any': Any,
        'src_Cc': Cc,
        'src_Cf': Cf,
        'src_P': P,
        'src_Z': Z,
    }

    # p{\Z\P\Cc\CF} (white spaces + control + format + punctuation)
    re_obj['src_ZPCc'] = '|'.join([re_obj['src_Any'], re_obj['src_P'], re_obj['src_Cc']])

    # \p{\Z\Cc} (white spaces + control)
    re_obj['src_ZCc'] = '|'.join([re_obj['src_Z'], re_obj['src_Cc']])

    # xperimental. List of chars, completely prohibited in links
    # because can separate it from other part of text

    text_separators = '[><\uff5c]'

    # All possible word characters (everything without punctuation, spaces & controls)
    # Defined via punctuation & spaces to save space
    # Should be something like \p{\L\N\S\M} (\w but without `_`)
    re_obj['src_pseudo_letter'] = '(?:(?!' + text_separators + '|' + re_obj['src_ZPCc'] + ')' + re_obj['src_Any'] + ')'

    # The same as abothe but without [0-9]
    # var src_pseudo_letter_non_d = '(?:(?![0-9]|' + src_ZPCc + ')' + src_Any + ')';

    re_obj['src_ip4'] = '(?:(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)'

    # Prohibit any of "@/[]()" in user/pass to avoid wrong domain fetch.
    re_obj['src_auth'] = '(?:(?:(?!' + re_obj['src_ZCc'] + '|[@/\\[\\]()]).)+@)?'
    re_obj['src_port'] = '(?::(?:6(?:[0-4]\\d{3}|5(?:[0-4]\\d{2}|5(?:[0-2]\\d|3[0-5])))|[1-5]?\\d{1,4}))?'

    re_obj['src_host_terminator'] = '(?=$|' + text_separators + '|' + re_obj[
        'src_ZPCc'] + ')(?!-|_|:\\d|\\.-|\\.(?!$|' + \
                                    re_obj['src_ZPCc'] + '))'

    # allow `I'm_king` if no pair found
    # github has ... in commit range links,
    # google has .... in links (issue #66)
    # Restrict to
    # - english
    # - percent-encoded
    # - parts of file path
    # until more examples found.
    re_obj['src_path'] = '(?:' + '[/?#]' + '(?:' + '(?!' + re_obj[
        'src_ZCc'] + '|' + text_separators + '|[()[\\]{}.,"\'?!\\-]).|''\\[(?:(?!' + re_obj[
                             'src_ZCc'] + '|\\]).)*\\]|' + '\\((?:(?!' + re_obj[
                             'src_ZCc'] + '|[)]).)*\\)|' + '\\{(?:(?!' + re_obj[
                             'src_ZCc'] + '|[}]).)*\\}|' + '\\"(?:(?!' + re_obj[
                             'src_ZCc'] + '|["]).)+\\"|' + "\\'(?:(?!" + re_obj['src_ZCc'] + "|[']).)+\\'|" + "\\'(?=" + \
                         re_obj['src_pseudo_letter'] + '|[-]).|' + '\\.{2,4}[a-zA-Z0-9%/]|' + '\\.(?!' + re_obj[
                             'src_ZCc'] + '|[.]).|' + '\\-(?!--(?:[^-]|$))(?:-*)|' if opts and opts[
        '---'] else '\\-+|''\\,(?!' + re_obj['src_ZCc'] + ').|''\\!(?!' + re_obj['src_ZCc'] + '|[!]).|' '\\?(?!' + \
                    re_obj['src_ZCc'] + '|[?]).'')+''|\\/' ')?'

    # Allow anything in markdown spec, forbid quote (") at the first position
    # because emails enclosed in quotes are far more common
    re_obj['src_email_name'] = '[\\-;:&=\\+\\$,\\.a-zA-Z0-9_][\\-;:&=\\+\\$,\\"\\.a-zA-Z0-9_]*'
    re_obj['src_xn'] = 'xn--[a-z0-9\\-]{1,59}'

    # More to read about domain names
    # http://serverfault.com/questions/638260/
    # Allow letters & digits (http://test1)
    re_obj['src_domain_root'] = '(?:' + re_obj['src_xn'] + '|' + re_obj['src_pseudo_letter'] + '{1,63}' + ')'
    # Don't need IP check, because digits are already allowed in normal domain names
    re_obj['src_host'] = '(?:' + '(?:(?:(?:' + re_obj['src_domain'] + ')\\.)*' + re_obj['src_domain'] + ')' + ')'

    re_obj['tpl_host_fuzzy'] = '(?:' + re_obj['src_ip4'] + '|' + '(?:(?:(?:' + re_obj[
        'src_domain'] + ')\\.)+(?:%TLDS%))' + ')'
    re_obj['tpl_host_no_ip_fuzzy'] = '(?:(?:(?:' + re_obj['src_domain'] + ')\\.)+(?:%TLDS%))'
    re_obj['src_host_strict '] = re_obj['src_host'] + re_obj['src_host_terminator']
    re_obj['tpl_host_fuzzy_strict'] = re_obj['tpl_host_fuzzy'] + re_obj['src_host_terminator']
    re_obj['src_host_port_strict'] = re_obj['src_host'] + re_obj['src_port'] + re_obj['src_host_terminator']
    re_obj['tpl_host_port_fuzzy_strict'] = re_obj['tpl_host_fuzzy'] + re_obj['src_port'] + re_obj['src_host_terminator']
    re_obj['tpl_host_port_no_ip_fuzzy_strict'] = re_obj['tpl_host_no_ip_fuzzy'] + re_obj['src_port'] + re_obj['src_host_terminator']

    # Main rules
    # Rude test fuzzy links by host, for quick deny
    re_obj['tpl_host_fuzzy_test']='localhost|www\\.|\\.\\d{1,3}\\.|(?:\\.(?:%TLDS%)(?:' + re_obj['src_ZPCc'] + '|>|$))'
    re_obj['tpl_email_fuzzy ']='(^|' + text_separators + '|"|\\(|' + re_obj['src_ZCc'] + ')' +'(' + re_obj['src_email_name'] + '@' + re_obj['tpl_host_fuzzy_strict'] + ')'
    # Fuzzy link can't be prepended with .:/\- and non punctuation.
    # but can start with > (markdown blockquote)
    re_obj['tpl_link_fuzzy ']='(^|(?![.:/\\-_@])(?:[$+<=>^`|\uff5c]|' + re_obj['src_ZPCc'] + '))' +'((?![$+<=>^`|\uff5c])' + re_obj['tpl_host_port_fuzzy_strict'] + re_obj['src_path'] + ')'
    # Fuzzy link can't be prepended with .:/\- and non punctuation.
    # but can start with > (markdown blockquote)
    re_obj['tpl_link_no_ip_fuzzy ']= '(^|(?![.:/\\-_@])(?:[$+<=>^`|\uff5c]|' + re_obj['src_ZPCc'] + '))' + '((?![$+<=>^`|\uff5c])' + re_obj['tpl_host_port_no_ip_fuzzy_strict'] + re_obj['src_path'] + ')';
    return re_obj
linkifyItRe({})
