def buildResponse(title, header, h1, body):
    """ Takes the values for a web page and builds a complete output """
    if type(body) is not list:
        body = [body]
    
    body = '\n'.join(body)
    response = html % (title, header, h1, body)
    return "HTTP/1.0 200 OK\r\nContent-type: text/html\r\nContent-length: %d\r\n\r\n%s" % (len(response), response)