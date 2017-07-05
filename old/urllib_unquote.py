"""Subset of the urllib I found here. Cut it down to save memory and to fix a stack overflow. Only the unquote module. https://github.com/lucien2k/wipy-urllib/blob/master/urllib.py"""

# FIXME I don't think I need this anymore.

def unquote(s):
    """ Kindly rewritten by Damien from Micropython
    No longer uses caching because of memory limitations """
    res = s.split('%')
    for i in range(1, len(res)):
        item = res[i]
        try:
            res[i] = chr(int(item[:2], 16)) + item[2:]
        except ValueError:
            res[i] = '%' + item
    return "".join(res)

def unquote_plus(s):
    """ Example: unquote('%7e/abc+def') -> '~/abc def' """
    s = s.replace('+', ' ')
    return unquote(s)