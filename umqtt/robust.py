# TODO I don't know how to do this any way but this, but this ruins making an
# easy update in the future; I cannot just download the new file.
from maintenance import maint
maint()

import utime
from . import simple

maint()

class MQTTClient(simple.MQTTClient):

    DELAY = 2
    DEBUG = False

    def delay(self, i):
        maint()
        utime.sleep(self.DELAY)

    def log(self, in_reconnect, e):
        maint()
        if self.DEBUG:
            if in_reconnect:
                print("mqtt reconnect: %r" % e)
            else:
                print("mqtt: %r" % e)

    def reconnect(self):
        maint()
        i = 0
        while 1:
            try:
                maint()
                return super().connect(False)
            except OSError as e:
                maint()
                self.log(True, e)
                i += 1
                self.delay(i)

    def publish(self, topic, msg, retain=False, qos=0):
        maint()
        while 1:
            try:
                maint()
                return super().publish(topic, msg, retain, qos)
            except OSError as e:
                maint()
                self.log(False, e)
            self.reconnect()

    def wait_msg(self):
        maint()
        while 1:
            try:
                maint()
                return super().wait_msg()
            except OSError as e:
                maint()
                self.log(False, e)
            self.reconnect()