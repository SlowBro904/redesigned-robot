def get_web_page_content(path, parameters)
    """ Gets our web page data. Configure this module for your URLs. """
    if path == '/':
        from webadmin.home import show
    
    # TODO I could probable create wifi/ and service_account/ subdirectories
    if path.startswith('/wifi_config'):
        from webadmin.wifi_config import show

    if path.startswith('/wifi_new_network'):
        from webadmin.wifi_new_network import show

    if path.startswith('/wifi_password'):
        from webadmin.wifi_password import show
    
    if path.startswith('/service_account_setup')
        from webadmin.service_account_setup import show
    
    if path.startswith('/service_account_save')
        from webadmin.service_account_save import show
   
    # Ignore anything else
    
    try:
        return show(parameters)
    except NameError:
        # Wrong web page
        return ''