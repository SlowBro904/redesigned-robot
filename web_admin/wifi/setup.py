def show(parameters):
    title = "Connect to a new Wi-Fi network"
    
    from config import config
    from maintenance import maint
    
    maint()
    
    ssid = None
    if 'ssid' in parameters and parameters['ssid']:
        ssid = parameters['ssid']
    
    if ssid == '*****Hidden_network*****':
        ssid = None
        hidden = True

    header = '''<script>
        function show_passwords() {
            document.getElementById('password1').style.display = "table-row";
            document.getElementById('password2').style.display = "table-row";
        }
        function hide_passwords() {
            document.getElementById('password1').style.display = "none";
            document.getElementById('password2').style.display = "none";
        }
        </script>'''

    h1 = title

    body = '''<form action='/wifi/save' method='get'>
    <table>'''

    sec_type = 'None'
    
    if ssid:
        sec_type = wifi.get_AP_sec_type(ssid)
        
        body += '''<tr><td>Network name (ssid): </td><td><div align='right'>'''
        body += ssid + "</div></td></tr>"
        body += "<input type='hidden' name='ssid' value='" + ssid + "' />"
        body += "<input type='hidden' name='sec_type' value='" + sec_type
        body += "' />"
    else:
        body += "<tr><td>Network name (ssid):</td><td><div align='right'>"
        body += "<input type='text' name='ssid' /></div></td></tr>"

        if hidden:
            body += "<input type='hidden' name='hidden' value='True' />"
        else:
            body += '''<tr><td>&nbsp;</td>
            <td><label><input type='checkbox' name='hidden' value='True'>Hidden
            </label>
            </td></tr>'''
        
        body += '''<tr><td>Security type: </td><td>
        <input type='radio' name='sec_type' value='None' 
            onclick='hide_passwords();'>None</input>
        <input type='radio' name='sec_type' value='WEP'  
            onclick='show_passwords();'>WEP</input>
        <input type='radio' name='sec_type' value='WPA'  
            onclick='show_passwords();'>WPA</input>
        <input type='radio' name='sec_type' value='WPA2' 
            onclick='show_passwords();'>WPA2</input>
        </td></tr>'''

    body += '''<tr id='password1' style='display:none'><td>Password: </td><td>
    <div align='right'><input type='password' name='password1'></div></td></tr>
    <tr id='password2' style='display:none'><td>Repeat password: </td><td>
    <div align='right'><input type='password' name='password2'></div></td></tr>
    <tr><td></td><td></td></tr>
    <tr><td></td><td><div align='right'><input type='submit' value='Next'>
    </div></td></tr>
    </table>
    </form>'''

    if sec_type != 'None':
        body += '''<script>show_passwords();</script>'''
    
    return (title, header, h1, body)
