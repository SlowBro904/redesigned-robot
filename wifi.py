import debugging
from network import WLAN
from config import config
from system import SystemCls
from maintenance import maint
    
class WIFI(object):
    def __init__(self, mode = 'STA', ant = None, power_save = None, 
                    debug = True, debug_level = 0):
        '''Sets up a Wi-Fi connection based on the mode.
        
        Mode may be one of 'STA', 'AP', or 'STA_AP'. Defaults to 'STA'.
        
        Can accept an ant type; either 'External' or 'Internal'.
        
        Accepts a value for STA power save; Either 'True' or 'False'. Only
        applicable in STA mode.
        '''
        if not ant:
            ant = config.conf['WIFI_ANTENNA']
        
        if not power_save:
            power_save = config.conf['WIFI_POWER_SAVE']
        
        # TODO Not working. I True here and it goes False elsewhere.
        debugging.enabled = debug
        debugging.default_level = debug_level
        self.debug = debugging.printmsg
        
        self._all_SSIDs = set()
        self.mode = self.mode2int(mode)
        self._all_APs = list()
        self.ant = self.ant2int(ant)
        self._conn_strength = None
        
        if self.mode is WLAN.STA:
            self.power_save = power_save
            self.wlan = WLAN(mode = self.mode, ant = self.ant, 
                                    power_save = power_save)
        else:
            # Either AP or STA_AP mode
            device_name = config.conf['DEVICE_NAME']

            # Access point SSID is the device name plus the last six digits of
            # the serial number. There may be more than one of my devices in
            # the area.
            # (I HOPE there's more than one of my devices in the area. Grin)
            ssid = device_name + '_' + SystemCls().serial[-6:]

            # AP or STA_AP mode
            password = config.conf['WEB_ADMIN_WIFI_PASSWORD']
            channel = int(config.conf['WEB_ADMIN_WIFI_CHANNEL'])
            sec_type_str = config.conf['WEB_ADMIN_WIFI_SECURITY_TYPE']
            sec_type = self.sec_type2int(sec_type_str)
            
            # When we set this up it automatically starts the access point on 
            # the specified ssid. When we do a connect() later it will connect
            # to the customer's router's ssid as well.
            self.wlan = WLAN(mode = self.mode, ssid = ssid, 
                                    auth = (sec_type, password),
                                    channel = channel, antenna = self.ant)
    
    
    @property
    def ssid(self):
        '''Sets the ssid variable'''
        return config.conf['WIFI_SSID']
    
    
    @property
    def sec_type(self):
        '''Sets the sec_type variable'''
        return self.sec_type2int(config.conf['WIFI_SECURITY_TYPE'])
    
    
    def sec_type2str(self, sec_type_int):
        '''Convert sec_type integer constant to human readable string'''
        sec_type = 'None'
        if sec_type_int == WLAN.WPA2:
            sec_type = 'WPA2'
        elif sec_type_int == WLAN.WPA:
            sec_type = 'WPA'
        elif sec_type_int == WLAN.WEP:
            sec_type = 'WEP'
        
        return sec_type
    
    
    def sec_type2int(self, sec_type):
        '''Convert sec_type human readable string to integer constant'''
        # FIXME I don't know the constant name for None; it's not in the docs
        result = 0
        if sec_type == 'WPA2':
            sec_type_int = WLAN.WPA2
        elif sec_type == 'WPA':
            sec_type_int = WLAN.WPA
        elif sec_type == 'WEP':
            sec_type_int = WLAN.WEP
        
        return sec_type_int
    
    
    def ant2int(self, ant):
        '''Convert antenna human readable string to integer constant'''
        # FIXME Look up a reasonable default, prefer one that does not exist
        ant_int = 0
        if ant == 'Internal':
            ant_int = WLAN.INT_ANT
        elif ant == 'External':
            ant_int = WLAN.EXT_ANT
        
        return ant_int
    
    
    def mode2int(self, mode):
        '''Convert mode human readable string to integer constant'''
        # FIXME Look up a reasonable default, prefer one that does not exist
        mode_int = 0
        if mode == 'STA':
            mode_int = WLAN.STA
        elif mode == 'AP':
            mode_int = WLAN.AP
        elif mode == 'STA_AP':
            mode_int = WLAN.STA_AP
        
        return mode_int
    
    
    def connect(self):
        '''Connect to the Wi-Fi network'''
        if self.wlan.isconnected():
            return True
        
        from machine import idle
        
        maint()
        
        password = config.conf['WIFI_PASSWORD']
        timeout = config.conf['WIFI_TIMEOUT']
        
        self.wlan.connect(self.ssid, auth=(self.sec_type, password),
                            timeout = timeout)
        
        # Save power while waiting
        while not self.wlan.isconnected():
            maint()
            idle()
        
        return self.wlan.isconnected()
    
    
    def disconnect(self):
        '''Disconnect from the Wi-Fi network'''
        maint()
        return self.wlan.disconnect()
    
    
    def isconnected(self):
        '''See if we are connected to the Wi-Fi network'''
        maint()
        return self.wlan.isconnected()
    
    
    def ifconfig(self, id = 0, ip = '', subnet_mask = '', gateway = '',
                    DNS_server = ''):
        '''Sets or returns the IP configuration in a tuple.
        
        (ip, subnet_mask, gateway, DNS_server)
        '''
        maint()
        
        # We don't always need gateway and DNS server
        if ip and subnet_mask:
            # TODO Do we even need subnet?
            self.wlan.ifconfig(id = id, config = (ip, subnet_mask, gateway,
                                DNS_server))
        
        # FIXME Comment
        print("self.wlan.ifconfig(" + str(id) + "): '" +
            str(self.wlan.ifconfig(id)) + "'")
        
        return self.wlan.ifconfig(id)
    
    
    @property
    def ip(self, id = 0):
        '''The IP address'''
        return self.ifconfig(id)[0]
    
    
    @property
    def all_APs(self):
        '''A list of all visible access points.
        
        It's sorted by signal strength with the strongest access points
        appearing first. Includes all values. (ssid, bssid, sec, channel, rssi)
        '''
        if not self._all_APs:
            # Sort on the RSSI (signal strength) which is in position [4] in 
            # the results from self.wlan.scan(), reversed so the largest 
            # strength comes first, since that's the strongest
            self._all_APs = sorted(self.wlan.scan(),
                                                key = lambda AP: AP[4],
                                                reverse=True)
        
        return self._all_APs
    
    
    def get_AP_sec_type(self, ssid):
        '''Takes an access point SSID, returns the security type in string
        form
        '''
        for AP in self.all_APs:
            this_ssid = AP[0]
            sec_type = AP[2]
            
            if this_ssid == ssid:
                return sec_type2str(sec_type)
    
    
    @property
    def all_SSIDs(self):
        '''A set of all visible SSIDs.

        It is derived from the set of access points. Whereas the set of APs
        gives all parameters such as the strength and BSSID, this gives only
        the SSIDs.
        
        As with the access points it is sorted by signal strength.
        '''
        if not self._all_SSIDs:
            for AP in self.all_APs:
                if not AP[0]:
                    # Skip blank SSIDs
                    continue
                
                self._all_SSIDs.add(AP[0])
        
        return self._all_SSIDs
    
    
    @property
    def conn_strength(self):
        '''The strength of our own connection'''
        # FIXME Does this work on hidden SSIDs?
        # Sets the variable when it matches self.ssid. If there are multiple
        # ssids in the area with the same name (xfinitywifi for example) we are
        # assuming that we are connected to the one with the greatest strength,
        # since that is most likely.
        if not self._conn_strength:
            for AP in self.all_APs:
                if AP[0] == self.ssid:
                    self.conn_strength = AP[4]
                    break
        return self._conn_strength

# End of class WIFI(object)


mywifi = None

def sta(debug = False):
    '''Sets up a connection as a station only, not an access point as well.
    
    Uses DHCP to get an IP.
    '''
    # Use the default config
    wifi = WIFI(debug = debug)
    return wifi


def sta_ap(debug = False):
    '''Sets up a connection that is both station and access point'''
    ip = config.conf['WEB_ADMIN_IP']
    subnet_mask = config.conf['WEB_ADMIN_SUBNET_MASK']
    gateway = config.conf['WEB_ADMIN_NETWORK_GATEWAY']
    DNS_server = config.conf['WEB_ADMIN_DNS_SERVER']
    
    # FIXME Set a default AP_PASSWORD at the factory and add to documentation, 
    # show in server web admin.
    # TODO Make it possible to change AP_PASSWORD.
    
    wifi = WIFI(mode = 'STA_AP', debug = debug)
    
    # 1 is for id = 1, the access point interface
    wifi.ifconfig(1, (ip, subnet_mask, gateway, DNS_server))
    
    return wifi