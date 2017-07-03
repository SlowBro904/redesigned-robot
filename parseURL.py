def parseURL(url):
    """ Parse the URL and return the path and get parameters """
    from ure import search as ure_search
    from urllib import unquote_plus
    
    if not url:
        return '/', ''

    path = ure_search("(.*?)(\?|$)", url).group(1)

    # Remove the path
    url = url.replace(path, '')

    # Remove the question mark delimiter, which may or may not now be at the beginning of url
    if url.startswith('?'):
        url = url[1:]

    # Drop off hashes
    url = url.replace("#.*$", '')

    vars = url.split('&')

    parameters = dict()
    if len(vars) > 0:
        for var in vars:
            if not var:
                # Next variable
                continue
            
            #vars = ure_search("(([^=]+)=((?:[^&]+|&amp;)*))", url)
            
            #if vars:
            keyname = unquote_plus(var.split('=')[0])
            value   = unquote_plus(var.split('=')[1])
            #parameters[vars.group(2)] = vars.group(3)
            #  url = url.replace(vars.group(0), '')
            parameters[keyname] = value
            #else: break

    return path, parameters