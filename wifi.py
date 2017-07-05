class WIFI(object):
    from wdt import wdt
    from network import WLAN
    from config import config
    
    # FIXME Add this. Hmm, I forget what we're supposed to do next. Google the phrases below since that should find them again.
    # Test needed to avoid losing connection after a soft reboot
    #if machine.reset_cause() != machine.SOFT_RESET:
    
    def __init__(self, mode = 'STA', antenna = self.config['WIFI_ANTENNA'], power_save = self.config['WIFI_POWER_SAVE']):
        """ Sets up a Wi-Fi connection based on the mode, which may be one of 'STA', 'AP', or 'STA_AP'. Defaults to 'STA'. Can accept an antenna type; either 'External' or 'Internal'. Accepts a value for STA power save; Either 'True' or 'False'. Only applicable in STA mode. """
        self.mode = mode2int(mode)
        self.antenna = self.antenna2int(antenna)
        
        if self.mode is not self.WLAN.STA:
            from serial import serial

            device_name = self.config['DEVICE_NAME']

            # Access point SSID is the device name plus the last six digits of the serial number. There may be more than one of my devices in the area.
            # (I HOPE there's more than one of my devices in the area. Grin)
            ssid = device_name + '_' + serial[-6:]

            # AP or STA_AP mode
            password = self.config['WEB_ADMIN_WIFI_PASSWORD']
            channel = int(self.config['WEB_ADMIN_WIFI_CHANNEL'])
            security_type = self.security_type2int(self.config['WEB_ADMIN_WIFI_SECURITY_TYPE'])
            
            # When we set this up it automatically starts the access point on the specified ssid. When we do a connect() later it will connect to the customer's router's ssid as well.
            self.wlan = self.WLAN(mode = self.mode, ssid = ssid, auth = (security_type, password), channel = channel, antenna = self.antenna)
        else:
            # STA mode
            self.power_save = True
            if power_save == 'False':
                self.power_save = False
            
            self.wlan = self.WLAN(mode = self.mode, antenna = self.antenna, power_save = self.power_save)
    
    
    @property
    def ssid(self):
        """ Sets the ssid variable """
        self.ssid = self.config['WIFI_SSID']
    
    
    @property
    def security_type(self):
        """ Sets the security_type variable """
        self.security_type = self.security_type2int(self.config['WIFI_SECURITY_TYPE'])
    
    
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
    
    
    def antenna2int(self, antenna):
        """ Convert human readable string to integer constant """
        antenna_int = 0 # FIXME Look up a reasonable default, prefer one that does not exist
        if antenna == 'Internal':
            antenna_int = self.WLAN.INT_ANT
        elif antenna == 'External':
            antenna_int = self.WLAN.EXT_ANT
        
        return antenna_int
    
    
    def mode2int(self, mode):
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
        if not self.ssid:
            return False
        
        from machine import idle
        
        self.wdt.feed()       
        
        password = self.config['WIFI_PASSWORD']
        timeout = self.config['WIFI_TIMEOUT']
        
        self.wlan.connect(self.ssid, auth=(self.security_type, password), timeout = timeout)
        
        while not self.wlan.isconnected(): # Save power while waiting
            self.wdt.feed() # FIXME Do I want to do this here, along with idle? Will that not save power?
            idle()
            # TODO Do I need to insert a sleep here?
        
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
    
    
    @property
    def all_access_points(self):
        """ A list of all visible access points, sorted by signal strength with the strongest access points appearing first. Includes all values (ssid, bssid, sec, channel, rssi) """
        # Sort on the RSSI (signal strength) which is in position [4] in the results from self.wlan.scan(), reversed so the largest strength comes first, since that's the strongest
        self.all_access_points = sorted(self.wlan.scan(), key = lambda AP: AP[4], reverse=True)
    
    
    def get_access_point_security_type(self, requested_ssid):
        """ Takes an access point SSID, returns the security type in string form """
        # FIXME May need to run security_type2str()
        for access_point in self.access_points:
            this_ssid = access_point[0]
            security_type = access_point[2]
            
            if this_ssid == requested_ssid:
                return security_type
    
    
    @property
    def all_ssids(self):
        """ A set of all visible SSIDs derived from the set of access points. Whereas the set of APs gives all parameters such as the strength and BSSID, this gives only the SSIDs. """
        # FIXME Does this run every time it is requested? Test. Want it to stay in memory and not go through fetching every time.
        self.all_ssids = set()
        
        for AP in self.all_access_points:
            if not AP[0]:
                # Skip blank SSIDs
                continue
            
            self.all_ssids.add(AP[0]) 
    
    
    @property
    def connection_strength(self):
        """ The strength of our own connection """
        # FIXME Does this work on hidden SSIDs?
        # Sets the variable when it matches self.ssid. If there are multiple ssids in the area with the same name (xfinitywifi for example) we are assuming that we are connected to the one with the greatest strength, since that is most likely.
        self.connection_strength = None
        for AP in self.all_access_points:
            if AP[0] == self.ssid:
                self.connection_strength = AP[4]
                break

# End of WIFI()


from config import config

wifi = None

def sta():
    """ Sets up a connection as a station only, not an access point as well. Uses DHCP to get an IP. """
    # TODO Add an IP configuration if customers demand it
    
    # Use the default config
    wifi = WIFI()
    return wifi


def sta_ap():
    """ Sets up a connection that is both station and access point """
    from config import config
    
    ip = config['WEB_ADMIN_IP']
    subnet_mask = config['WEB_ADMIN_SUBNET_MASK']
    gateway = config['WEB_ADMIN_NETWORK_GATEWAY']
    DNS_server = config['WEB_ADMIN_DNS_SERVER']

    # FIXME Set a default AP_PASSWORD at the factory and add to documentation, show in server web admin.
    # TODO Make it possible to change AP_PASSWORD.

    wifi = WIFI(mode = 'STA_AP')
    
    # id = 1 is the access point interface
    wifi.ifconfig(id = 1, config = (ip, subnet_mask, gateway, DNS_server))
    
    return wifi