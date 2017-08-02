from wifi import wifi
from network import WLAN
from config import config
print("Starting test_wifi")

def good(msg):
    print("[SUCCESS] " + str(msg))

wifi = wifi.sta_ap()
assert wifi.ssid == config['WIFI_SSID'], "WIFI_SSID"
good("WIFI_SSID")
ip = config.conf['WEB_ADMIN_IP']
assert ip is not None, "WEB_ADMIN_IP"
good("WEB_ADMIN_IP")
subnet_mask = config.conf['WEB_ADMIN_SUBNET_MASK']
assert subnet_mask is not None, "WEB_ADMIN_SUBNET_MASK"
good("WEB_ADMIN_SUBNET_MASK")
gateway = config.conf['WEB_ADMIN_NETWORK_GATEWAY']
assert gateway is not None, "WEB_ADMIN_NETWORK_GATEWAY"
good("WEB_ADMIN_NETWORK_GATEWAY")
DNS_server = config.conf['WEB_ADMIN_DNS_SERVER']
assert DNS_server is not None, "WEB_ADMIN_DNS_SERVER"
good("WEB_ADMIN_DNS_SERVER")
assert wifi.sec_type2int('WPA') == WLAN.WPA2, "sec_type2int()"
good("sec_type2int()")
assert 'WPA' == wifi.sec_type2str(WLAN.WPA2), "sec_type2str()"
good("sec_type2str()")
assert wifi.ant2int(WLAN.EXT_ANT) == 'External', "ant2int()"
good("ant2int()")
assert wifi.mode2int('STA_AP') == WLAN.STA_AP, "mode2int()"
good("mode2int()")
assert wifi.ifconfig == ('', '', '', ''), "Non-connected ifconfig()"
good("Non-connected ifconfig()")
assert wifi.connect() is True, "connect()"
good("connect()")
assert wifi.disconnect() is True, "disconnect()"
good("disconnect()")
wifi.connect()
assert wifi.isconnected() is True, "isconnected()"
good("isconnected()")
assert wifi.ifconfig() == (ip, subnet_mask, gateway, DNS_server), "ifconfig()"
good("ifconfig()")
assert wifi.ip == ip, "Cannot get IP"
good("Got the IP")
assert len(wifi.all_APs) > 0, "all_APs"
good("all_APs")
assert wifi.get_AP_sec_type('xfinitywifi') == 'None', "get_AP_sec_type()"
good("get_AP_sec_type()")
assert len(wifi.all_SSIDs) > 0, "all_SSIDs"
good("all_SSIDs")
assert len(wifi.all_APs) >= len(wifi.all_SSIDs), "all_SSIDs list not right"
good("all_SSIDs list correct length")
assert wifi.conn_strength < 0, "conn_strength >= 0"
good("conn_strength < 0")