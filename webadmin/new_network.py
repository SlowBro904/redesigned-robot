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
body.append("""<form action='/password' id='password' method='get'>
<table>""")
if SSID:
    body.append("<tr><td>Network name (SSID): </td><td><div align='right'>" + SSID + """</div></td></tr>
    <input type='hidden' name='SSID' value=\"" + SSID + "\" />
    <input type='hidden' name='STA_security_type' value=\"""" + str(STA_security_type[0]) + "\" />")
else:
    body.append("<tr><td>Network name (SSID):</td><td><div align='right'><input type='text' name='SSID'></div></td></tr>")
    if hidden:
        body.append("<input type='hidden' name='hidden' value=\"true\" />")
    else:
        body.append("""<tr><td>&nbsp;</td>
        <td><label><input type='checkbox' name='hidden' value=\"true\">Hidden</label>
        </td></tr>""")
    
    body.append("""<tr><td>Security type: </td><td>
    <input type='radio' name='STA_security_type' value=\"None\" onclick='hide_passwords();'>None</input>
    <input type='radio' name='STA_security_type' value=\"WEP\"  onclick='show_passwords();'>WEP</input>
    <input type='radio' name='STA_security_type' value=\"WPA\"  onclick='show_passwords();'>WPA</input>
    <input type='radio' name='STA_security_type' value=\"WPA2\"  onclick='show_passwords();'>WPA2</input>
    </td></tr>""")
body.append("""<tr id='password1' style='display:none'><td>Password: </td><td><div align='right'><input type='password' name='password1'></div></td></tr>
<tr id='password2' style='display:none'><td>Repeat password: </td><td><div align='right'><input type='password' name='password2'></div></td></tr>
<tr><td></td><td></td></tr>""")

body.append("""<tr><td></td><td><div align='right'><input type='submit' value='Next' onClick='encapsulate_passwords();'></div></td></tr>
</form>
</table>""")

if STA_security_type != 'None':
    body.append("<script>show_passwords();</script>")