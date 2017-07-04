title = "SB" # FIXME Change
h1 = title
if wifi.isconnected():
    # FIXME Get connection strength
    body += connected_section
    body.append("""<a href='/wifi'>Connect to another network</a><br />
    <br />
    <a href=''>Change username or password</a><br />
    <br />
    Version """ + open('/flash/version.txt').read().strip() + " | Serial number " + str(hexlify(unique_id()), 'utf-8') + "<br />")
else:
    body.append("""Let's get started!<br />
    <script>window.location.href = '/wifi';</script>""")
