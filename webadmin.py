from wifi import wifi
from config import config
from machine import reset
# TODO Which urllib*.py file do I need? Delete the one I don't need.
from parseURL import parseURL
from ure import search as ure_search
from usocket import getaddrinfo, socket
from buildResponse import buildResponse
# FIXME Re-add the thread but how do I deal with getting updates in the middle of viewing the web interface?

port = config['WEB_ADMIN_PORT']

html = """<!DOCTYPE html>
<html>
    <head>
    <title>%s</title> 
    %s
    </head>
    <body> <h1>%s</h1>
    %s
    </body>
</html>"""

addr = getaddrinfo('10.1.1.1', port)[0][-1]

s = socket()
s.bind(addr)
s.listen(1)

# FIXME Add a debug option
print('Web admin interface listening on ' + addr[0] + ", port " + str(port))

# Sort on the RSSI (signal strength)
all_APs = sorted(wifi.scan(), key = lambda AP: AP[4], reverse=True)
all_SSIDs = list()
WiFi_strength = ""
for AP in all_APs:
    SSID = AP[0]
    if SSID == STA_SSID:
        if not WiFi_strength:
            WiFi_strength = str(AP[4]) # TODO Fails on a hidden SSID FIXME Does it work on a visible one?
    all_SSIDs.append(SSID)

connected_section = list()
connected_section.append("Connnected to " + STA_SSID + "<br />")
if WiFi_strength:
    connected_section.append("Strength: " + WiFi_strength + "<br />")

connected_section.append("IP address: " + wifi.ifconfig()[0] + "<br />")

while True:
    cl, addr = s.accept()
    print('Client ' + str(addr[0]) + ' connected')
    cl_file = cl.makefile('wb')
    request = ""
    raw_request = ""
    while True:
        line = cl_file.readline()
        match = ure_search('GET (.*?) HTTP\/1\.1', str(line))    
        if match:
            raw_request = line
            request = match.group(1)
        if not line or line == b'\r\n': break
    
    path, parameters = parseURL(request)
    
    print("path: '" + str(path) + "'")
    print("parameters: '" + str(parameters) + "'")
    
    hidden = False
    if 'hidden' in parameters and parameters['hidden'] == 'true':
        hidden = True
    
    SSID = False
    if 'SSID' in parameters and parameters['SSID']:
        SSID = parameters['SSID']
    
    if SSID == '*****Hidden_network*****':
        SSID = ''
        hidden = True
    
    password1 = ""
    if 'password1' in parameters and parameters['password1']:
        password1 = parameters['password1']
    
    password2 = ""
    if 'password2' in parameters and parameters['password2']:
        password2 = parameters['password2']
    
    if 'STA_security_type' in parameters and parameters['STA_security_type']:
        STA_security_type = parameters['STA_security_type']
    
    title   = ""
    header  = ""
    h1      = ""
    body    = list()
    if path == "/":
        import webadmin.index
    elif path.startswith("/wifi"):
        import webadmin.wifi
    elif path.startswith("/new_network"):
        import webadmin.new_network
    elif path.startswith('/password'):
        import webadmin.password
    else: # Ignore anything else
        cl_file.close()
        cl.close()
        # Start the loop over
        continue
    
    cl.send(buildResponse(title, header, h1, body))
    cl_file.close()
    cl.close()