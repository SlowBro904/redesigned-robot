from network import WLAN
from config import config
from test_suite import good
from wifi import mywifi, sta_ap
print("Starting test_wifi")

mywifi = sta_ap(debug = True)
assert mywifi.ssid == config.conf['WIFI_SSID'], "WIFI_SSID"
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
assert mywifi.sec_type2int('WPA2') == WLAN.WPA2, "sec_type2int()"
good("sec_type2int()")
assert 'WPA2' == mywifi.sec_type2str(WLAN.WPA2), "sec_type2str()"
good("sec_type2str()")
assert mywifi.ant2int('External') == WLAN.EXT_ANT, "ant2int()"
good("ant2int()")
assert mywifi.mode2int('STA_AP') == WLAN.STA_AP, "mode2int()"
good("mode2int()")
assert mywifi.ifconfig() == ('0.0.0.0', '0.0.0.0', '0.0.0.0', '0.0.0.0'), (
    "Non-connected ifconfig()")
good("Non-connected ifconfig()")
assert mywifi.connect() is True, "connect()"
good("connect()")
assert mywifi.disconnect() is None, "disconnect()"
good("disconnect()")
mywifi.connect()
assert mywifi.isconnected() is True, "isconnected()"
good("isconnected()")

# FIXME Comment
print("---------------------")
print("ip: '" + str(ip) + "'")
print("subnet_mask: '" + str(subnet_mask) + "'")
print("gateway: '" + str(gateway) + "'")
print("DNS_server: '" + str(DNS_server) + "'")

# FIXME It reverts to 192.168.4.1
assert mywifi.ifconfig(1) == (ip, subnet_mask, gateway, DNS_server), (
    "ifconfig()")
good("ifconfig()")
assert mywifi.ip == ip, "Cannot get IP"
good("Got the IP")
assert len(mywifi.all_APs) > 0, "all_APs"
good("all_APs")
assert mywifi.get_AP_sec_type('xfinitywifi') == 'None', "get_AP_sec_type()"
good("get_AP_sec_type()")
assert len(mywifi.all_SSIDs) > 0, "all_SSIDs"
good("all_SSIDs")
assert len(mywifi.all_APs) >= len(mywifi.all_SSIDs), "all_SSIDs list not right"
good("all_SSIDs list correct length")
assert mywifi.conn_strength < 0, "conn_strength >= 0"
good("conn_strength < 0")