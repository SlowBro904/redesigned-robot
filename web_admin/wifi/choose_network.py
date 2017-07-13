def show(parameters):
    title = "Wi-Fi configuration"
    
    from wifi import wifi
    from maintenance import maintenance
    
    maintenance()
    
    h1 = title
    body = ""
    
    if wifi.ssid:
        body += "Current Wi-Fi network: " + wifi.ssid + "<br /><br />"
    
    if wifi.ip:
        body += "IP address: " + wifi.ip + "<br /><br />"
    
    body += """<br />
    <form action='/wifi/setup' method='get'>
    Connect to a new Wi-Fi network: <select name='ssid'>"""
    
    for this_ssid in wifi.all_ssids:
        if this_ssid == wifi.ssid:
            # Skip my own
            continue
        
        body += "  <option value='" + this_ssid + "'>" + this_ssid + "</option>"
    
    body += """  <option value='*****N/A*****'>---</option>
      <option value='*****Hidden_network*****'>Hidden network</option>
    </select> <input type='submit' value='Next' /></form>"""
    
    return (title, header, h1, body)