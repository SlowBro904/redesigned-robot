def show(parameters):
    '''Save the service account username and password'''
    from config import config
    from reboot import reboot
    from maintenance import maint
    
    maint()
    
    email = None
    if 'email' in parameters and parameters['email']:
        email = parameters['email']
    
    password1 = ''
    if 'password1' in parameters and parameters['password1']:
        password1 = parameters['password1']
    
    password2 = ''
    if 'password2' in parameters and parameters['password2']:
        password2 = parameters['password2']
    
    
    title = "Please wait..."
    header = ""
    h1 = title
    body = ""
    
    if not password1:
        body += '''Missing the password<br />
        <button onclick='window.history.back();'>Go back</button>'''
        
        return (title, header, h1, body)
    
    if password1 != password2:
        body += '''Passwords don't match<br />
        <button onclick='window.history.back();'>Go back</button>'''
        
        return (title, header, h1, body)
    
    try:
        config.update(('SERVICE_ACCOUNT_EMAIL', email),
                        ('SERVICE_ACCOUNT_PASSWORD', password1))
    except:
        body += '''There was some problem writing the config file. Try again or
        contact technical support.<br />
        <button onclick='window.history.back();'>Go back</button>'''
    
    body += "<meta http-equiv='refresh' content='0;url=/' />"

    return (title, header, h1, body)