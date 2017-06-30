from wifi import get_wifi_config, get_security_type_int, connect
from usocket import getaddrinfo, socket
from machine import unique_id, reset, idle
from _thread import start_new_thread
from ure import search as ure_search
from urllib import unquote_plus
from ubinascii import hexlify
from network import WLAN

# Last six digits of the unique ID. There may be more than one SB in the area. I HOPE there's more than one SB in the area. Grin
# FIXME Change to the actual name (not SB_XXXXXX)
AP_SSID = 'SB_' + str(hexlify(unique_id())[-6:], 'utf-8')
# FIXME Use the same as the person's service password
AP_password = '123456abcdef'
# FIXME Add an antenna selector
wlan = WLAN(mode = WLAN.STA_AP, ssid = AP_SSID, auth = (WLAN.WPA2, AP_password), antenna = WLAN.INT_ANT, power_save = True)
# FIXME Go with a 2-host but easy to remember subnet. Since I want 10.10.10.10 the DHCP server defaults to handing out 10.10.10.11 which is the broadcast for this subnet.
wlan.ifconfig(id = 1, config = ('10.10.10.10', '255.255.255.0', '0.0.0.0', '0.0.0.0'))

# TODO Do I really need to repeat myself here? This code is in wifi.py. DRY. Maybe need to see how to make it work in both places. A class maybe. But wait -- is this really repeating myself? I'm doing STA_AP and that's different.
wifi_config_file = '/flash/wifi.cfg'
STA_SSID, STA_password, STA_security_type = get_wifi_config(wifi_config_file)

if STA_SSID:
    wlan.connect(ssid = STA_SSID, auth = (get_security_type_int(STA_security_type), STA_password), timeout=30000)
    while not wlan.isconnected(): idle() # Save power while waiting
    print("STA IP address: " + str(wlan.ifconfig()[0]))

port = 80

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

def parseURL(url):
    ''' Parse the URL and return the path and get parameters '''
    if not url: return '/', ''

    path = ure_search("(.*?)(\?|$)", url).group(1)

    # Remove the path
    url = url.replace(path, '')

    # Remove the question mark delimiter, which may or may not now be at the beginning of url
    if url.startswith('?'): url = url[1:]

    # Drop off hashes
    url = url.replace("#.*$", '')

    vars = url.split('&')

    parameters = dict()
    if len(vars) > 0:
        for var in vars:
            if not var: continue
            #vars = ure_search("(([^=]+)=((?:[^&]+|&amp;)*))", url)
            #if vars:
            keyname = unquote_plus(var.split('=')[0])
            value   = unquote_plus(var.split('=')[1])
            #parameters[vars.group(2)] = vars.group(3)
            #  url = url.replace(vars.group(0), '')
            parameters[keyname] = value
            #else: break

    return path, parameters

def buildResponse(title, header, h1, body):
    ''' Takes the values for a web page and builds a complete output '''
    if type(body) is not list: body = [body]
    body = '\n'.join(body)
    response = html % (title, header, h1, body)
    return "HTTP/1.0 200 OK\r\nContent-type: text/html\r\nContent-length: %d\r\n\r\n%s" % (len(response), response)

# FIXME Don't listen always, only when booted by power button
# FIXME Uncomment
#addr = getaddrinfo('10.10.10.10', port)[0][-1]
#FIXME Remove
addr = getaddrinfo('0.0.0.0', port)[0][-1]

s = socket()
s.bind(addr)
s.listen(1)

# FIXME Add a debug option
print('Web admin interface listening on ' + addr[0] + ", port " + str(port))

# Sort on the RSSI (signal strength)
all_APs = sorted(wlan.scan(), key = lambda AP: AP[4], reverse=True)
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
if WiFi_strength: connected_section.append("Strength: " + WiFi_strength + "<br />")
connected_section.append("IP address: " + wlan.ifconfig()[0] + "<br />")

def main():
    ''' The main loop '''
    global STA_security_type
    
    # TODO Move all these into separate files? Or not?
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
        if 'hidden' in parameters and parameters['hidden'] == 'true': hidden = True
        SSID = False
        if 'SSID' in parameters and parameters['SSID']: SSID = parameters['SSID']
        if SSID == '*****Hidden_network*****':
            SSID = ''
            hidden = True
        password1 = ""
        if 'password1' in parameters and parameters['password1']: password1 = parameters['password1']
        password2 = ""
        if 'password2' in parameters and parameters['password2']: password2 = parameters['password2']
        if 'STA_security_type' in parameters and parameters['STA_security_type']: STA_security_type = parameters['STA_security_type']
        
        title   = ""
        header  = ""
        h1      = ""
        body    = list()
        if path == "/":
            title = "SB" # FIXME Change
            h1 = title
            if wlan.isconnected():
                # FIXME Get connection strength
                body += connected_section
                body.append("<a href='/wifi'>Connect to another network</a><br />")
                body.append("<br />")
                body.append("<a href=''>Change username or password</a><br />")
                body.append("<br />")
                body.append("Version " + open('/flash/version.txt').read().strip() + " | Serial number " + str(hexlify(unique_id()), 'utf-8') + "<br />")
            else:
                body.append("Let's get started!<br />")
                body.append("<script>window.location.href = '/wifi';</script>")
        elif path.startswith("/wifi"):
            title = "Wi-Fi configuration"
            h1 = title
            body += connected_section
            body.append("<br />")
            body.append("<form action='/new_network' method='get'>")
            # FIXME Add a try/except for if the STA_SSID variable is not set. Make sure it's at least an empty string ""
            if STA_SSID: body.append("Connect to another network: <select name='SSID'>")
            else: body.append("Connect to a wireless network: <select name='SSID'>")
            for this_SSID in all_SSIDs:
                if not this_SSID: continue # Skip blank/hidden
                if this_SSID == STA_SSID: continue # Skip my own
                this_SSID = this_SSID.replace('\\:', ':')
                body.append("  <option value=\"" + this_SSID + "\">" + this_SSID + "</option>")
            # FIXME Add detection for this
            body.append("  <option value=\"*****N/A*****\">---</option>")
            body.append("  <option value=\"*****Hidden_network*****\">Hidden network</option>")
            body.append("</select> <input type='submit' value='Next' /></form>")
        elif path.startswith("/new_network"):
            title = "Connect to new network"
            header = """<script>
                function show_passwords() {
                    document.getElementById('password1').style.display = "table-row";
                    document.getElementById('password2').style.display = "table-row";
                }
                function hide_passwords() {
                    document.getElementById('password1').style.display = "none";
                    document.getElementById('password2').style.display = "none";
                }
                </script>"""
            h1 = title
            body.append("<form action='/password' id='password' method='get'>")
            body.append("<table>")
            if SSID:
                body.append("<tr><td>Network name (SSID): </td><td><div align='right'>" + SSID + "</div></td></tr>")
                body.append("<input type='hidden' name='SSID' value=\"" + SSID + "\" />")
                body.append("<input type='hidden' name='STA_security_type' value=\"" + str(STA_security_type[0]) + "\" />")
            else:
                body.append("<tr><td>Network name (SSID):</td><td><div align='right'><input type='text' name='SSID'></div></td></tr>")
                if hidden:
                    body.append("<input type='hidden' name='hidden' value=\"true\" />")
                else:
                    body.append("<tr><td>&nbsp;</td>")
                    body.append("<td><label><input type='checkbox' name='hidden' value=\"true\">Hidden</label>")
                    body.append("</td></tr>")
                
                body.append("<tr><td>Security type: </td><td>")
                body.append("<input type='radio' name='STA_security_type' value=\"None\" onclick='hide_passwords();'>None</input> ")
                body.append("<input type='radio' name='STA_security_type' value=\"WEP\"  onclick='show_passwords();'>WEP</input> ")
                body.append("<input type='radio' name='STA_security_type' value=\"WPA\"  onclick='show_passwords();'>WPA</input>")
                body.append("<input type='radio' name='STA_security_type' value=\"WPA2\"  onclick='show_passwords();'>WPA2</input>")
                body.append("</td></tr>")
            body.append("<tr id='password1' style='display:none'><td>Password: </td><td><div align='right'><input type='password' name='password1'></div></td></tr>")
            body.append("<tr id='password2' style='display:none'><td>Repeat password: </td><td><div align='right'><input type='password' name='password2'></div></td></tr>")
            body.append("<tr><td></td><td></td></tr>")

            body.append("<tr><td></td><td><div align='right'><input type='submit' value='Next' onClick='encapsulate_passwords();'></div></td></tr>")
            body.append("</form>")
            body.append("</table>")
            if STA_security_type != 'None': body.append("<script>show_passwords();</script>")
        elif path.startswith('/password'):
            title = "Saving network configuration"
            h1 = title
            if not SSID:
                body.append("Missing the SSID<br />")
                body.append("<button onclick='window.history.back();'>Go back</button>")
                cl.send(buildResponse(title, header, h1, body))
                cl_file.close()
                cl.close()
                continue
            
            if STA_security_type not in ["None", "WEP", "WPA", "WPA2"]:
                body.append("Missing the security type<br />")
                body.append("<button onclick='window.history.back();'>Go back</button>")
                cl.send(buildResponse(title, header, h1, body))
                cl_file.close()
                cl.close()
                continue
            
            # The password might be empty so don't check that it was passed, only that it matches
            if password1 != password2:
                body.append("Passwords don't match<br />")
                body.append("<button onclick='window.history.back();'>Go back</button>")
                cl.send(buildResponse(title, header, h1, body))
                cl_file.close()
                cl.close()
                continue
            
            try:
                wifi_config_fileH = open(wifi_config_file, 'w')
                write_bytes = wifi_config_fileH.write("SSID = " + SSID + "\n")
                write_bytes = wifi_config_fileH.write("PASSWORD = " + password1 + "\n")
                write_bytes = wifi_config_fileH.write("WIFI_SECURITY_TYPE = " + STA_security_type + "\n")
                wifi_config_fileH.close()
            except:
                body.append("There was some problem writing the config file. Try again or contact technical support.<br />")
                body.append("<button onclick='window.history.back();'>Go back</button>")
                cl.send(buildResponse(title, header, h1, body))
                cl_file.close()
                cl.close()
                continue
            
            #if not connect():
            #    body.append("Saved the configuration but unable to connect to the network. Try again or contact technical support.<br />")
            #    body.append("<button onclick='window.history.back();'>Go back</button>")
            #    cl.send(buildResponse(title, header, h1, body))
            #    cl_file.close()
            #    cl.close()
            #    continue
            
            #my_IP = wlan.ifconfig()
            #if len(my_IP) > 0:
            #    if my_IP[0] is '0.0.0.0':
            #        body.append("Requested an IP but did not get one. Try again or contact technical support.<br />")
            #        body.append("<button onclick='window.history.back();'>Go back</button>")
            #    cl.send(buildResponse(title, header, h1, body))
            #    cl_file.close()
            #    cl.close()
            #    continue
            
            body.append('Saving, please wait...<br />')
            body.append('<meta http-equiv="refresh" content="15;url=/" />')
            cl.send(buildResponse(title, header, h1, body))
            cl_file.close()
            cl.close()
            # Reboot
            reset()
        else: # Ignore anything else
            cl_file.close()
            cl.close()
            continue
        cl.send(buildResponse(title, header, h1, body))
        cl_file.close()
        cl.close()

start_new_thread(main, ())