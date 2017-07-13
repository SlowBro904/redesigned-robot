def start():
    """Start the web admin interface"""
    from maintenance import maintenance
    from _thread import start_new_thread
    
    maintenance()
    
    # Fork a new thread so we can get back to the next step in our process
    start_new_thread(_daemon, (run = True))


def stop():
    """Stop the web admin interface"""
    from maintenance import maintenance
    
    maintenance()
    self._daemon(run = False)


def _daemon(run = True):
    """The actual web server process.
    
    Don't run this directly; use start() instead.
    """
    from config import config
    from machine import Timer
    from urllib import unquote_plus
    from re import search as re_search
    from maintenance import maintenance
    from socket import getaddrinfo, socket
    from urls import get_web_page_content
    
    maintenance()
    
    timeout = config['WEB_ADMIN_DAEMON_TIMEOUT']
    timer = Timer.Chrono()
    
    with open(config['WEB_ADMIN_TEMPLATE_FILE']) as templateH:
        template = templateH.readlines()

    # Start our web server
    ip = config['WEB_ADMIN_IP']
    port = config['WEB_ADMIN_PORT']
    
    # TODO Is getaddrinfo() really needed? Bind() just needs the ip and port.
    mysocket = socket().bind(getaddrinfo(ip, port)[0][-1]).listen(1)
    mysocket.settimeout(timeout)
    
    timer.start()
    
    # TODO A kludge until Pycom fixes _thread.exit() from outside the thread
    global _run
    _run = run
    while _run:
        maintenance()
        
        # Listen on our socket for incoming requests
        # FIXME Will this trigger a wdt? Should we setblocking(False)? Test it.
        # Try a very long timeout with a very short wdt.
        # https://www.scottklement.com/rpg/socktut/nonblocking.html
        try:
            conn = mysocket.accept()[0]
        except mysocket.timeout:
            break
        
        # We just got a request. Reset our timer.
        timer.reset()
        maintenance()
        
        # Create a file handle on our incoming request
        connH = conn.makefile('wb')
        
        # We have an incoming browser request, pull out just the relevant info 
        # from the GET line
        request = ""
        while True:
            line = str(connH.readline())
            match = re_search('GET (.*?) HTTP\/1\.1', line)    
            if match:
                request = match.group(1)
            
            # If we're at the end of our request exit the loop
            if not line or line == b'\r\n':
                break
        
        maintenance()
        
        # If we don't have any request for some reason default to the root 
        # directory with no parameters
        if not request:
            path, parameters = ('/', dict())
        else:
            # Path is everything before the question mark in the URL
            path = re_search("(.*?)(\?|$)", request).group(1)

            # Pull the path out of our request
            request = request.replace(path, '')

            # Drop off hashes, which we don't need
            request = request.replace("#.*$", '')
            
            # Remove the question mark delimiter, which may or may not now be at
            # the beginning of url
            if request.startswith('?'):
                request = request[1:]
            
            parameters = dict()
            
            # Split the remainder of our request into variables
            for var in request.split('&'):
                # TODO I don't think this is needed anymore
                #if not var:
                #    # Next variable
                #    continue
                
                # Split this variable into parameter and value using the 
                # unquote_plus function
                parameter = unquote_plus(var.split('=')[0])
                value = unquote_plus(var.split('=')[1])
                
                # Add to our dictionary
                parameters[parameter] = value
        
        maintenance()
        
        web_page_content = get_web_page_content(path, parameters)
        
        if web_page_content:
            # Load web_page_content into our template
            web_page_content = template % (web_page_content)
            
            data = 'HTTP/1.0 200 OK\r\n'
            data += 'Content-type: text/html\r\n'
            data += 'Content-length: ' + str(len(web_page_content)) + '\r\n'
            data += '\r\n'
            data += web_page_content
            
            conn.send(data)
        
        maintenance()
        
        # Close up our requests
        connH.close()
        conn.close()
        
        if timer.read() >= timeout:
            break
    
    timer.stop()
    maintenance()
    mysocket.close()