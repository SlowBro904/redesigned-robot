title = "Wi-Fi configuration"
h1 = title
body += connected_section
body.append("""<br />
<form action='/new_network' method='get'>""")
# FIXME Add a try/except for if the STA_SSID variable is not set. Make sure it's at least an empty string ""
if STA_SSID:
    body.append("Connect to another network: <select name='SSID'>")
else:
    body.append("Connect to a wireless network: <select name='SSID'>")

for this_SSID in all_SSIDs:
    if not this_SSID:
        # Skip blank/hidden
        continue
    
    if this_SSID == STA_SSID:
        # Skip my own
        continue
    
    this_SSID = this_SSID.replace('\\:', ':')
    body.append("  <option value=\"" + this_SSID + "\">" + this_SSID + "</option>")

# FIXME Add detection for this (uh... for what?)
body.append("""  <option value=\"*****N/A*****\">---</option>
  <option value=\"*****Hidden_network*****\">Hidden network</option>
</select> <input type='submit' value='Next' /></form>""")