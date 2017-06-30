class WIFI(object):
    from network import WLAN
    from wdt import wdt
    
    
    # FIXME Add. Test needed to avoid losing connection after a soft reboot
    #if machine.reset_cause() != machine.SOFT_RESET:
    
    def __init__(self):
        """ Sets up a Wi-Fi connection """
        from config import config
        
        self.SSID = config['WIFI_SSID']
        self.password = config['WIFI_PASSWORD']
        self.security_type = config['WIFI_SECURITY_TYPE']
        
        self.wlan = self.WLAN(mode = self.WLAN.STA)
    
    
    def security_type2str(self, security_type):
        """ Convert integer constant to human readable string """
        result = 'None'
        if  security_type == self.WLAN.WPA2:
            result == 'WPA2'
        elif security_type == self.WLAN.WPA:
            result == 'WPA'
        elif security_type == self.WLAN.WEP:
            result == 'WEP'
        
        return result
    
    
    def security_type2int(self, security_type):
        """ Convert human readable string to integer constant """
        result = 0 # FIXME I don't know the constant name for None; it's not in the docs
        if  security_type == 'WPA2':
            result = self.WLAN.WPA2
        elif security_type == 'WPA':
            result = self.WLAN.WPA
        elif security_type == 'WEP':
            result = self.WLAN.WEP
        
        return result
    
    
    def connect(self):
        """ Connect to the Wi-Fi network """
        from machine import idle
        # Convert to integer constant
        security_type_int = self.security_type2int(self.security_type)
        
        self.wdt.feed()
        try:
            self.wlan.connect(self.SSID, auth=(security_type_int), self.password), timeout = 10000)
        except:
            pass
        
        while not self.wlan.isconnected(): # Save power while waiting
            self.wdt.feed() # FIXME Do I want to do this here, along with idle? Will that not save power?
            idle()
            # TODO Do I need to insert a sleep here?
        
        self.wlan.init(power_save = True)
        
        return self.wlan.isconnected()
    
    
    def disconnect(self):
        """ Disconnect from the Wi-Fi network """
        self.wdt.feed()
        return self.wlan.disconnect()
    
    
    def isconnected(self):
        """ See if we are connected to the Wi-Fi network """
        self.wdt.feed()
        return self.wlan.isconnected()
    
    
    def ifconfig(self, ip = '', subnet_mask = '', gateway = '', DNS_server = ''):
        """ Sets or returns the IP configuration in a tuple. (ip, subnet_mask, gateway, DNS_server) """
        self.wdt.feed()
        
        if ip and subnet_mask: # We don't always need gateway and DNS server.
            # TODO Do we even need subnet?
            try:
                self.wlan.ifconfig(config = (ip, subnet_mask, gateway, DNS_server))
            except:
                pass

        try:
            return self.wlan.ifconfig()
        except:
            return ('','','','') # TODO Is this redundant? Try the output of the command above
    
    
    @property
    def ip(self):
        """ The IP address """
        # FIXME Integrate into webadmin.py
        self.ip = self.ifconfig()[0]