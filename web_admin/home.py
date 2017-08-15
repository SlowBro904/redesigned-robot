def show(parameters):
    '''The home page'''
    from wifi import wifi
    from config import config
    from system import System
    from maintenance import maint
    
    device_name = config.conf['DEVICE_NAME']
    title = device_name
    header = ""
    h1 = title
    body = ""
    
    serial = System().serial
    version = System().version
    
    maint()

    if not wifi.ssid:
        body += '''Let's get started!
        <script>window.location.href = '/wifi/choose_network';</script>'''
    elif not wifi.isconnected():
        body += '''I cannot connect to your home router.<br />
        <br />
        <ul>
        <li>Is the <a href='/wifi/choose_network'>Wi-Fi configuration</a>
        correct?</li>
        <li>If you are still unable to connect, contact technical support.</li>
        <ul>'''
    elif not cloud.ping():
        body += "I could not connect to the " + device_name + '''
        network.<br />
        <br />
        <ul>
        <li>Is your home router's internet connection working? Check
        that you can get to the internet using another device. Try resetting
        your router.</li>
        <li>Try resetting your ''' + device_name + '''.</li>
        <li>If you are still unable to connect, contact technical support.</li>
        </ul>'''
    elif not cloud.can_login():
        body += "I could not login to the " + device_name + ''' network.<br />
        <br />
        <ul>
        <li>Did your username or password recently change?
        <a href='/service_account/setup'>Please update it</a>.</li>
        <li>Is your account still active? Please login to the ''' + device_name
        + ''' website.</li>
        <li>If you are still unable to connect, contact technical support.</li>
        </ul>'''
    elif not cloud.encryption_working():
        body += "I could not communicate with the " + device_name + ''' 
        network. There is some problem with the encryption key. Please contact
        technical support.'''
    else:
        body += '''Connnected to the ''' + device_name + ''' network.<br />
        <br />
        <a href='/wifi/choose_network'>Configure Wi-Fi</a><br />
        <br />
        <a href='/service_account/setup'>Update your ''' + device_name 
        + ''' service username or password</a>'''
    
    body += '''<br />
    <br />
    <a href='/error_log'>Error log</a><br />
    <br />
    ''' + device_name + " software version " + version + " | " +
    " Serial number " + serial
    
    return (title, header, h1, body)