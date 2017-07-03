""" A wifi module which can be imported into other modules to prevent re-initializing the object every time. """
from config import config
from wifi_class import WIFI

wifi = None

def sta():
    # The default config
    return WIFI()


def sta_ap():
    from machine import unique_id
    from ubinascii import hexlify
    # Last six digits of the unique ID. There may be more than one of my devices in the area.
    # I HOPE there's more than one of my devices in the area. Grin
    AP_SSID = config['AP_SSID_PREFIX'] + '_' + str(hexlify(unique_id())[-6:], 'utf-8')

    # FIXME Set a default AP_PASSWORD at the factory and add to documentation, show in server web admin.
    # TODO Make it possible to change AP_PASSWORD.

    wifi = WIFI(mode = 'STA_AP', ssid = AP_SSID, password = config['AP_PASSWORD'])
    wifi.ifconfig(id = 1, config = ('10.1.1.1', '255.255.255.252', '0.0.0.0', '0.0.0.0'))
    return wifi