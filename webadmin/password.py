title = "Saving network configuration"
h1 = title
if not SSID:
    body.append("""Missing the SSID<br />
    <button onclick='window.history.back();'>Go back</button>""")
    cl.send(buildResponse(title, header, h1, body))
    cl_file.close()
    cl.close()
    continue

if STA_security_type not in ["None", "WEP", "WPA", "WPA2"]:
    body.append("""Missing the security type<br />
    <button onclick='window.history.back();'>Go back</button>""")
    cl.send(buildResponse(title, header, h1, body))
    cl_file.close()
    cl.close()
    continue

# The password might be empty so don't check that it was passed, only that it matches
if password1 != password2:
    body.append("""Passwords don't match<br />
    <button onclick='window.history.back();'>Go back</button>""")
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
    body.append("""There was some problem writing the config file. Try again or contact technical support.<br />
    <button onclick='window.history.back();'>Go back</button>""")
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

#my_IP = wifi.ifconfig()
#if len(my_IP) > 0:
#    if my_IP[0] is '0.0.0.0':
#        body.append("Requested an IP but did not get one. Try again or contact technical support.<br />")
#        body.append("<button onclick='window.history.back();'>Go back</button>")
#    cl.send(buildResponse(title, header, h1, body))
#    cl_file.close()
#    cl.close()
#    continue

body.append("""Saving, please wait...<br />
<meta http-equiv="refresh" content="15;url=/" />""")
cl.send(buildResponse(title, header, h1, body))
cl_file.close()
cl.close()
# Reboot
reset()