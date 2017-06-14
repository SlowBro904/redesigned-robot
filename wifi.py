class WIFI(object):
  from network import WLAN
  from machine import idle
  from main import config
  
  def __init__(self, SSID = None, password = None, security_type = None):
    """ Sets up a Wi-Fi connection """
    if not SSID:
      self.SSID = self.config['WIFI_SSID']
      self.password = self.config['WIFI_PASSWORD']
      self.security_type = self.config['WIFI_SECURITY_TYPE']
    
    self.wlan = self.WLAN(mode=WLAN.STA)
    self.connect()
  
  
  def security_type2str(self, security_type):
    """ Convert integer constant to human readable string """
    result = 'None'
    if    security_type == self.WLAN.WPA2:
        result == 'WPA2'
    elif  security_type == self.WLAN.WPA:
        result == 'WPA'
    elif  security_type == self.WLAN.WEP:
        result == 'WEP'
    
    return result
  
  
  def security_type2int(self, security_type):
    """ Convert human readable string to integer constant """
    result = 0 # FIXME I don't know the constant name for None; it's not in the docs
    if    security_type == 'WPA2':
        result = self.WLAN.WPA2
    elif  security_type == 'WPA':
        result = self.WLAN.WPA
    elif  security_type == 'WEP':
        result = self.WLAN.WEP
    
    return result
  
  
  def connect(self):
    # Convert to integer constant
    security_type_int = self.security_type2int(self.security_type)
    
    try:
        self.wlan.connect(self.SSID, auth=(security_type_int), self.password), timeout=10000)
    except:
        pass
    
    idle() while not self.wlan.isconnected() # Save power while waiting
    
    self.wlan.init(power_save=True)
    
    return self.wlan.isconnected()
  
  
    def disconnect(self):
        return self.wlan.disconnect()
  
  
    def isconnected(self):
        return self.wlan.isconnected()
  
  
    def ifconfig(self, ip = '', subnet_mask = '', gateway = '', DNS_server = ''):
        """ Sets or returns the IP configuration in a tuple. (ip, subnet_mask, gateway, DNS_server) """
        if ip and subnet_mask: # We don't always need gateway and DNS server.
        # TODO Do we even need subnet?
        try:
            self.wlan.ifconfig(config=(ip, subnet_mask, gateway, DNS_server))
        except:
            pass
    
        try:
            return self.wlan.ifconfig()
        except:
            return ('','','','') # TODO Is this redundant
  
  
  @property
  def ip(self):
    # FIXME Integrate into webadmin.py
    self.ip = self.ifconfig()[0]