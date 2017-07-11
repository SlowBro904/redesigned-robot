def show(parameters):
    """The home page"""
    from wifi import wifi
    from config import config
    from system import SYSTEM
    from maintenance import maintenance
    
    device_name = config['DEVICE_NAME']
    title = device_name
    header = ""
    h1 = title
    
    serial = SYSTEM().serial
    version = SYSTEM().version
    
    maintenance()
    
    if not wifi.ssid:
        body = """Let's get started!<br />
        <script>window.location.href = '/wifi/choose_network';</script>"""
    else:
        body = "Connnected to " + wifi.ssid + "<br />"
        
        if wifi.isconnected():
            if wifi.connection_strength:
                body += "Strength: " + wifi.connection_strength + "<br />"
            
            if wifi.ip:
                body += "IP address: " + wifi.ip + "<br />"
        
        body += """<br />
        <a href='/wifi/choose_network'>Connect to another network</a><br />
        <br />
        <a href='/service_account/setup'>Update your """ + device_name 
        body += """ service username or password</a><br />
        <br />
        <a href='/error_log'>Error log</a><br />
        <br />
        <a href='/advanced/setup'>Advanced</a><br />
        <br />
        Version """ + version + """ | Serial number """ + serial + """<br />"""
    
    return (title, header, h1, body)