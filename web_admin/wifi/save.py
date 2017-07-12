def show(parameters):
    """Save the Wi-Fi password and configuration"""
    from wifi import wifi
    from config import config
    from reboot import reboot
    from maintenance import maintenance
    
    maintenance()
    
    ssid = None
    if 'ssid' in parameters and parameters['ssid']:
        ssid = parameters['ssid']
        
    hidden = False
    if 'hidden' in parameters and parameters['hidden'] == 'True':
        hidden = True
    
    password1 = ''
    if 'password1' in parameters and parameters['password1']:
        password1 = parameters['password1']
    
    password2 = ''
    if 'password2' in parameters and parameters['password2']:
        password2 = parameters['password2']
    
    security_type = ''
    if 'security_type' in parameters and parameters['security_type']:
        security_type = parameters['security_type']
    
    title = "Please wait..."
    header = ""
    h1 = title
    body = ""

    if not ssid:
        body += """Missing the SSID<br />
        <button onclick='window.history.back();'>Go back</button>"""
        
        return (title, header, h1, body)

    if security_type not in ['None', 'WEP', 'WPA', 'WPA2']:
        body += """Missing the security type<br />
        <button onclick='window.history.back();'>Go back</button>"""
        
        return (title, header, h1, body)

    # The password might be empty so don't check that it was passed, only that
    # it matches
    if password1 != password2:
        body += """Passwords don't match<br />
        <button onclick='window.history.back();'>Go back</button>"""
        
        return (title, header, h1, body)

    try:
        config.update(('WIFI_SSID', ssid), ('WIFI_PASSWORD', password1),
                        ('WIFI_SECURITY_TYPE', security_type))
    except:
        body += """There was some problem writing the config file. Try again or 
        contact technical support.<br />
        <button onclick='window.history.back();'>Go back</button>"""
        
        return (title, header, h1, body)
    
    wifi.connect()
    
    if config['SERVICE_ACCOUNT_EMAIL']:
        body += "<meta http-equiv='refresh' content='10;url=/' />"
    else:
        # Service account not setup yet
        body += """<meta http-equiv='refresh' 
        content='0;url=/service_account/setup' />"""
    
    return (title, header, h1, body)