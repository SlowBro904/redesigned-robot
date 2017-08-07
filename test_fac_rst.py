print("Starting test_fac_rst")
import fac_rst
import test_suite
from time import sleep
from config import config
from uos import rename, remove

good = test_suite.good

rename('/flash/config.json', '/flash/config.good.json')
with open('/flash/config.good.json') as d:
    with open('/flash/config.json', 'w') as c:
        c.write(d.read())

try:
    test_str = 'Config file updated'
    config.update({"XYZ": test_str})
    assert config.conf["XYZ"] == test_str, "config.update()"
    good("config.update()")
    fac_rst.fac_rst_pin_lsnr(True)
    print("Sleeping four seconds...")
    sleep(4)
    fac_rst.fac_rst_pin_lsnr(False)
    assert config.conf["XYZ"] == test_str, "Did fac_rst before five seconds"
    good("Didn't reset at four seconds")
    fac_rst.fac_rst_pin_lsnr(True)
    print("Sleeping six seconds...")
    sleep(6)
    fac_rst.fac_rst_pin_lsnr(False)
    assert config.conf["XYZ"] == None, "fac_rst failed"
    good("fac_rst")
finally:
    with open('/flash/config.good.json') as g:
        with open('/flash/config.json', 'w') as c:
            c.write(g.read())
    remove('/flash/config.good.json')