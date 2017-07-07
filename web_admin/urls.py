def get_web_page_content(path, parameters)
    """Gets our web page data.
    
    Configure this module for your URLs.
    """
    from maintenance import maintenance
    
    maintenance()

    if path == '/':
        from webadmin.home import show
    
    # TODO I could probable create wifi/ and service_account/ subdirectories
    if path.startswith('/wifi/config'):
        from webadmin.wifi.config import show

    if path.startswith('/wifi/new_network'):
        from webadmin.wifi.new_network import show

    if path.startswith('/wifi/password'):
        from webadmin.wifi.password import show
    
    if path.startswith('/service_account/setup')
        from webadmin.service_account.setup import show
    
    if path.startswith('/service_account/save')
        from webadmin.service_account.save import show
    
    if path.startswith('/error_log')
        from webadmin.error_log import show
   
    # Ignore anything else
    
    try:
        return show(parameters)
    except NameError:
        # Wrong web page
        return ''