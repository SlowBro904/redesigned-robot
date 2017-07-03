class WIFI(object):
    from wdt import wdt
    from network import WLAN
    from config import config
    
    # FIXME Add this. Hmm, I forget what we're supposed to do next. Google the phrases below since that should find them again.
    # Test needed to avoid losing connection after a soft reboot
    #if machine.reset_cause() != machine.SOFT_RESET:
    
    # TODO Break this into multiple lines
    def __init__(self, mode = WLAN.STA, ssid = self.config['WIFI_SSID'], password = self.config['WIFI_PASSWORD'], security_type = self.config['WIFI_SECURITY_TYPE'], connection_timeout = self.config['WIFI_CONNECTION_TIMEOUT'], antenna = self.config['WIFI_ANTENNA'], power_save = self.config['WIFI_POWER_SAVE']):
        """ Sets up a Wi-Fi connection """
        self.mode = mode
        self.ssid = ssid
        self.antenna = antenna
        self.password = password
        self.power_save = power_save
        self.security_type = security_type
        self.connection_timeout = connection_timeout
    
        self.wlan = self.WLAN()
    
    
    def security_type2str(self, security_type_int):
        """ Convert integer constant to human readable string """
        security_type = 'None'
        if security_type_int == self.WLAN.WPA2:
            security_type == 'WPA2'
        elif security_type_int == self.WLAN.WPA:
            security_type == 'WPA'
        elif security_type_int == self.WLAN.WEP:
            security_type == 'WEP'
        
        return security_type
    
    
    def security_type2int(self, security_type):
        """ Convert human readable string to integer constant """
        result = 0 # FIXME I don't know the constant name for None; it's not in the docs
        if security_type == 'WPA2':
            security_type_int = self.WLAN.WPA2
        elif security_type == 'WPA':
            security_type_int = self.WLAN.WPA
        elif security_type == 'WEP':
            security_type_int = self.WLAN.WEP
        
        return security_type_int
    
    
    def antenna_type2int(self, antenna):
        """ Convert human readable string to integer constant """
        antenna_int = 0 # FIXME Look up a reasonable default, prefer one that does not exist
        if antenna == 'Internal':
            antenna_int = self.WLAN.INT_ANT
        elif antenna == 'External':
            antenna_int = self.WLAN.EXT_ANT
        
        return antenna_int
    
    
    def mode_type2int(self, mode):
        """ Convert human readable string to integer constant """
        mode_int = 0 # FIXME Look up a reasonable default, prefer one that does not exist
        if mode == 'STA':
            mode_int = self.WLAN.STA
        elif mode == 'AP':
            mode_int = self.WLAN.AP
        elif mode == 'STA_AP':
            mode_int = self.WLAN.STA_AP
        
        return mode_int
    
    
    def connect(self):
        """ Connect to the Wi-Fi network """
        from machine import idle
        
        ssid = self.ssid
        password = self.password
        power_save = self.power_save
        connection_timeout = self.connection_timeout
        
        # Convert to integer constants
        mode = self.mode_type2int(self.mode)
        antenna = self.antenna_type2int(self.antenna)
        security_type = self.security_type2int(self.security_type)
        
        self.wdt.feed()

        try:
            self.wlan.connect(ssid, auth=(security_type, password), timeout = connection_timeout)
        except:
            pass
        
        while not self.wlan.isconnected(): # Save power while waiting
            self.wdt.feed() # FIXME Do I want to do this here, along with idle? Will that not save power?
            idle()
            # TODO Do I need to insert a sleep here?
        
        if power_save == 'True':
            self.wlan.init(power_save = power_save)
        
        return self.wlan.isconnected()
    
    
    def disconnect(self):
        """ Disconnect from the Wi-Fi network """
        self.wdt.feed()
        return self.wlan.disconnect()
    
    
    def isconnected(self):
        """ See if we are connected to the Wi-Fi network """
        self.wdt.feed()
        return self.wlan.isconnected()
    
    
    def ifconfig(self, id = 0, ip = '', subnet_mask = '', gateway = '', DNS_server = ''):
        """ Sets or returns the IP configuration in a tuple. (ip, subnet_mask, gateway, DNS_server) """
        self.wdt.feed()
        
        if ip and subnet_mask: # We don't always need gateway and DNS server.
            # TODO Do we even need subnet?
            self.wlan.ifconfig(id = id, config = (ip, subnet_mask, gateway, DNS_server))

        try:
            return self.wlan.ifconfig()
        except:
            return ('','','','') # TODO Is this redundant? Try the output of the command above
    
    
    @property
    def ip(self):
        """ The IP address """
        # FIXME Integrate into webadmin.py
        self.ip = self.ifconfig()[0]