from errors import Errors

errors = Errors()

def status():
    '''Returns True if running'''
    global _run
    return _run


def start():
    '''Start the web admin interface'''
    from maintenance import maintenance
    from _thread import start_new_thread
    
    maintenance()
    
    try:
        # Fork a new thread so we can get back to the next step in our process
        run = True
        return start_new_thread(_daemon, (run,))
    except:
        warning = ("Could not start the web admin.",
                    " ('web_admin/__init__.py', 'start')")
        errors.warning(warning)
        return False


def stop():
    '''Stop the web admin interface'''
    from maintenance import maintenance
    
    maintenance()
    run = False
    return self._daemon(run,)


def _daemon(run = True):
    '''The actual web server process.
    
    Don't run this directly; use start() instead.
    '''
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
    
    try:
        with open(config['WEB_ADMIN_TEMPLATE_FILE']) as templateH:
            template = templateH.readlines()
    except OSError:
        warning = ("Could not load the web admin template.",
                    " ('web_admin/__init__.py', '_daemon')")
        errors.warning(warning)
        return False

    # Start our web server
    ip = config['WEB_ADMIN_IP']
    port = config['WEB_ADMIN_PORT']
    
    try:
        # TODO Is getaddrinfo() really needed? Bind() just needs the ip & port.        
        mysocket.bind(getaddrinfo(ip, port)[0][-1])
        # TODO Should I leave this to the default? I only want one client.
        mysocket.listen(1)
        mysocket.settimeout(timeout)
    except:
        warning = ("Could not load the web admin template.",
                    " ('web_admin/__init__.py', '_daemon')")
        errors.warning(warning)
        return False
    
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
        # FIXME AttributeError: 'socket' object has no attribute 'timeout'
        except mysocket.timeout:
            break
        
        # We just got a request. Reset our timer.
        timer.reset()
        maintenance()
        
        # Create a file handle on our incoming request
        try:
            connH = conn.makefile('wb')
        except:
            # TODO Also a 500 error or equivalent. Also add 40* and 50* errors.
            warning = ("Web admin socket failure.",
                        " ('web_admin/__init__.py', '_daemon')")
            errors.warning(warning)
            break
        
        # We have an incoming browser request, pull out just the relevant info 
        # from the GET line
        request = ""
        while True:
            line = str(connH.readline())
            match = re_search('GET (.*?) HTTP\/1\.1', line)    
            if match:
                # FIXME I think I want the break below this?
                request = match.group(1)
            
            # If we're at the end of our request exit the loop
            # FIXME I think I want to remove this?
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
            
            # Remove the question mark delimiter, which may or may not now be
            # at the beginning of url
            if request.startswith('?'):
                request = request[1:]
            
            parameters = dict()
            
            # Split the remainder of our request into variables
            for var in request.split('&'):
                # TODO I don't think this is needed anymore
                if not var:
                    # Next variable
                    continue
                
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
            
            try:
                conn.send(data)
            except:
                warning = ("Web admin socket failure.",
                            " ('web_admin/__init__.py', '_daemon')")
                errors.warning(warning)
                break
        
        maintenance()
        
        try:
            # Close up our requests
            connH.close()
            conn.close()
        except:
            # Ignore errors
            pass
        
        if timer.read() >= timeout:
            break
    
    try:
        timer.stop()
        maintenance()
        mysocket.close()
    except:
        # Ignore errors
        pass