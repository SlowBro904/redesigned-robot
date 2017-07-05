def show(parameters):
    """ The home page """
    from wifi import wifi
    from config import config
    from serial import serial
    from version import version
    
    device_name = config['DEVICE_NAME']
    title = device_name
    header = ""
    h1 = title
    
    if not wifi.ssid:
        body = """Let's get started!<br />
        <script>window.location.href = '/wifi';</script>"""
    else:
        body = "Connnected to " + wifi.ssid + "<br />"
        
        if wifi.isconnected():
            if wifi.connection_strength:
                body += "Strength: " + wifi.connection_strength + "<br />"
            
            if wifi.ip:
                body += "IP address: " + wifi.ip + "<br />"
        
        body += """<br />
        <a href='/wifi_config'>Connect to another network</a><br />
        <br />
        <a href='/service_account'>Update your """ + device_name + """ service username or password</a><br />
        <br />
        Version """ + version + """ | Serial number """ + serial + """<br />"""
    
    return (title, header, h1, body)