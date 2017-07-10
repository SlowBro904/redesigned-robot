def get_web_page_content(path, parameters)
    """Gets our web page data.
    
    Configure this module for your URLs.
    """
    from maintenance import maintenance
    
    maintenance()

    if path == '/':
        from webadmin.home import show
    
    if path.startswith('/wifi/choose_network'):
        from webadmin.wifi.choose_network import show

    if path.startswith('/wifi/setup'):
        from webadmin.wifi.setup import show

    if path.startswith('/wifi/save'):
        from webadmin.wifi.save import show
    
    if path.startswith('/service_account/setup')
        from webadmin.service_account.setup import show
    
    if path.startswith('/service_account/save')
        from webadmin.service_account.save import show
    
    if path.startswith('/error_log')
        from webadmin.error_log import show
    
    if path.startswith('/advanced/setup')
        from webadmin.advanced.setup import show
    
    if path.startswith('/advanced/save')
        from webadmin.advanced.save import show
   
    # Ignore anything else
    
    try:
        return show(parameters)
    except NameError:
        # Wrong web page
        return ''