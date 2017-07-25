def show(parameters):
    '''Save the advanced page'''
    from maintenance import maint
    
    maint()
    
    title = "Please wait..."
    header = ""
    h1 = title
    body = ""
    
    key1 = ''
    if 'key1' in parameters and parameters['key1']:
        key1 = parameters['key1']
    
    key2 = ''
    if 'key2' in parameters and parameters['key2']:
        key2 = parameters['key2']
    
    if not key1:
        body += '''Missing the key<br />
        <button onclick='window.history.back();'>Go back</button>'''
        
        return (title, header, h1, body)
    
    if key1 != key2:
        body += '''Keys don't match<br />
        <button onclick='window.history.back();'>Go back</button>'''
        
        return (title, header, h1, body)
    
    try:
        config.update(('ENCRYPTION_KEY', key1))
    except:
        body += '''There was some problem writing the config file. Try again or 
        contact technical support.<br />
        <button onclick='window.history.back();'>Go back</button>'''
        
        return (title, header, h1, body)
    
    body += "<meta http-equiv='refresh' content='5;url=/' />"
    
    return (title, header, h1, body)