""" A web admin interface """
from config import config
from urllib import unquote_plus
from re import search as re_search
from _thread import start_new_thread
from socket import getaddrinfo, socket
from webadmin.urls import get_web_page_content
# FIXME Re-add the thread but how do I deal with getting updates in the middle of viewing the web interface? Use locking or a global variable maybe. Maybe I don't get updates while booting from the power button. No, I should; how else are they going to get updates with customer support?

with open(config['WEB_ADMIN_TEMPLATE_FILE']) as templateH:
    template = templateH.readlines()

# Start our web server
addr = getaddrinfo(config['WEB_ADMIN_IP'], config['WEB_ADMIN_PORT'])[0][-1]
s = socket()
s.bind(addr)
s.listen(1)

def main():
    while True:
        # Listen on our socket for incoming requests
        cl, addr = s.accept()
        
        # Create a file handle on our incoming request
        cl_file = cl.makefile('wb')

        # We have an incoming browser request, pull out just the relevant info from the GET line
        request = ""
        while True:
            line = str(cl_file.readline())
            match = re_search('GET (.*?) HTTP\/1\.1', line)    
            if match:
                request = match.group(1)
            
            # If we're at the end of our request exit the loop
            if not line or line == b'\r\n':
                break
        
        # If we don't have any request default to the root directory with no parameters
        if not request:
            path, parameters = ('/', dict())
        else:
            # Path is everything before the question mark in the URL
            path = re_search("(.*?)(\?|$)", request).group(1)

            # Pull the path out of our request
            request = request.replace(path, '')

            # Drop off hashes, which we don't need
            request = request.replace("#.*$", '')
            
            # Remove the question mark delimiter, which may or may not now be at the beginning of url
            if request.startswith('?'):
                request = request[1:]
            
            parameters = dict()
            
            # Split the remainder of our request into variables
            for var in request.split('&'):
                # TODO I don't think this is needed anymore
                #if not var:
                #    # Next variable
                #    continue
                
                # Split this variable into parameter and value using the unquote_plus function
                parameter = unquote_plus(var.split('=')[0])
                value = unquote_plus(var.split('=')[1])
                
                # Add to our dictionary
                parameters[parameter] = value
        
        web_page_content = get_web_page_content(path, parameters)
        
        if web_page_content:
            # Load web_page_content into our template
            web_page_content = template % (web_page_content)
            
            # len(web_page_content) sets the Content-length header
            # FIXME Is it counting from zero like len() and if not does it cut off our data at the end?
            cl.send("HTTP/1.0 200 OK\r\nContent-type: text/html\r\nContent-length: %d\r\n\r\n%s" % (len(web_page_content), web_page_content)
        
        # Close up our requests
        cl_file.close()
        cl.close()

# Multithreading so we can get back to the next step in our process
# FIXME Be sure we time out and deep sleep after some time
start_new_thread(main, ())