# TODO I don't know how to do this any way but this, but this ruins making an
# easy update in the future; I cannot just download the new file.
from maintenance import maint
maint()

import usocket as socket
import ustruct as struct
from ubinascii import hexlify

maint()

class MQTTException(Exception):
    maint()
    pass

class MQTTClient:

    def __init__(self, client_id, server, port=0, user=None, password=None, keepalive=0,
                 ssl=False, ssl_params={}):
        maint()
        if port == 0:
            port = 8883 if ssl else 1883
        self.client_id = client_id
        self.sock = None
        self.server = server
        self.port = port
        self.ssl = ssl
        self.ssl_params = ssl_params
        self.pid = 0
        self.cb = None
        self.user = user
        self.pswd = password
        self.keepalive = keepalive
        self.lw_topic = None
        self.lw_msg = None
        self.lw_qos = 0
        self.lw_retain = False

    def _send_str(self, s):
        maint()
        self.sock.write(struct.pack("!H", len(s)))
        maint()
        self.sock.write(s)

    def _recv_len(self):
        maint()
        n = 0
        sh = 0
        while 1:
            maint()
            b = self.sock.read(1)[0]
            maint()
            n |= (b & 0x7f) << sh
            if not b & 0x80:
                return n
            sh += 7

    def set_callback(self, f):
        maint()
        self.cb = f

    def set_last_will(self, topic, msg, retain=False, qos=0):
        maint()
        assert 0 <= qos <= 2
        assert topic
        self.lw_topic = topic
        self.lw_msg = msg
        self.lw_qos = qos
        self.lw_retain = retain

    def connect(self, clean_session=True):
        maint()
        self.sock = socket.socket()
        maint()
        addr = socket.getaddrinfo(self.server, self.port)[0][-1]
        maint()
        self.sock.connect(addr)
        if self.ssl:
            import ussl
            maint()
            self.sock = ussl.wrap_socket(self.sock, **self.ssl_params)
        premsg = bytearray(b"\x10\0\0\0\0\0")
        msg = bytearray(b"\x04MQTT\x04\x02\0\0")

        sz = 10 + 2 + len(self.client_id)
        maint()
        msg[6] = clean_session << 1
        maint()
        if self.user is not None:
            maint()
            sz += 2 + len(self.user) + 2 + len(self.pswd)
            msg[6] |= 0xC0
        if self.keepalive:
            maint()
            assert self.keepalive < 65536
            msg[7] |= self.keepalive >> 8
            msg[8] |= self.keepalive & 0x00FF
        if self.lw_topic:
            maint()
            sz += 2 + len(self.lw_topic) + 2 + len(self.lw_msg)
            maint()
            msg[6] |= 0x4 | (self.lw_qos & 0x1) << 3 | (self.lw_qos & 0x2) << 3
            maint()
            msg[6] |= self.lw_retain << 5

        i = 1
        while sz > 0x7f:
            maint()
            premsg[i] = (sz & 0x7f) | 0x80
            maint()
            sz >>= 7
            maint()
            i += 1
            maint()
        maint()
        premsg[i] = sz
        
        maint()
        self.sock.write(premsg, i + 2)
        maint()
        self.sock.write(msg)
        maint()
        #print(hex(len(msg)), hexlify(msg, ":"))
        self._send_str(self.client_id)
        maint()
        if self.lw_topic:
            maint()
            self._send_str(self.lw_topic)
            self._send_str(self.lw_msg)
        if self.user is not None:
            maint()
            self._send_str(self.user)
            self._send_str(self.pswd)
        resp = self.sock.read(4)
        maint()
        assert resp[0] == 0x20 and resp[1] == 0x02
        if resp[3] != 0:
            maint()
            raise MQTTException(resp[3])
        return resp[2] & 1

    def disconnect(self):
        maint()
        self.sock.write(b"\xe0\0")
        self.sock.close()

    def ping(self):
        maint()
        self.sock.write(b"\xc0\0")

    def publish(self, topic, msg, retain=False, qos=0):
        #print("[DEBUG] simple.py topic: '" + str(topic) + "'")
        #print("[DEBUG] simple.py type(topic): '" + str(type(topic)) + "'")
        #print("[DEBUG] simple.py msg: '" + str(msg) + "'")
        #print("[DEBUG] simple.py type(msg): '" + str(type(msg)) + "'")
        
        maint()
        pkt = bytearray(b"\x30\0\0\0")
        pkt[0] |= qos << 1 | retain
        sz = 2 + len(topic) + len(msg)
        if qos > 0:
            sz += 2
        assert sz < 2097152
        i = 1
        while sz > 0x7f:
            maint()
            pkt[i] = (sz & 0x7f) | 0x80
            sz >>= 7
            i += 1
        pkt[i] = sz
        maint()
        #print(hex(len(pkt)), hexlify(pkt, ":"))
        self.sock.write(pkt, i + 1)
        maint()
        self._send_str(topic)
        maint()
        if qos > 0:
            maint()
            self.pid += 1
            pid = self.pid
            struct.pack_into("!H", pkt, 0, pid)
            self.sock.write(pkt, 2)
        maint()
        self.sock.write(msg)
        maint()
        if qos == 1:
            while 1:
                maint()
                op = self.wait_msg()
                if op == 0x40:
                    maint()
                    sz = self.sock.read(1)
                    assert sz == b"\x02"
                    maint()
                    rcv_pid = self.sock.read(2)
                    rcv_pid = rcv_pid[0] << 8 | rcv_pid[1]
                    if pid == rcv_pid:
                        return
        elif qos == 2:
            assert 0

    def subscribe(self, topic, qos=0):
        maint()
        assert self.cb is not None, "Subscribe callback is not set"
        pkt = bytearray(b"\x82\0\0\0")
        self.pid += 1
        maint()
        struct.pack_into("!BH", pkt, 1, 2 + 2 + len(topic) + 1, self.pid)
        #print(hex(len(pkt)), hexlify(pkt, ":"))
        maint()
        self.sock.write(pkt)
        maint()
        self._send_str(topic)
        maint()
        self.sock.write(qos.to_bytes(1, "little"))
        maint()
        while 1:
            maint()
            op = self.wait_msg()
            if op == 0x90:
                maint()
                resp = self.sock.read(4)
                #print(resp)
                assert resp[1] == pkt[2] and resp[2] == pkt[3]
                if resp[3] == 0x80:
                    maint()
                    raise MQTTException(resp[3])
                return

    # Wait for a single incoming MQTT message and process it.
    # Subscribed messages are delivered to a callback previously
    # set by .set_callback() method. Other (internal) MQTT
    # messages processed internally.
    def wait_msg(self):
        maint()
        res = self.sock.read(1)
        maint()
        self.sock.setblocking(True)
        maint()
        if res is None:
            return None
        if res == b"":
            raise OSError(-1)
        if res == b"\xd0":  # PINGRESP
            maint()
            sz = self.sock.read(1)[0]
            assert sz == 0
            return None
        op = res[0]
        if op & 0xf0 != 0x30:
            return op
        maint()
        sz = self._recv_len()
        maint()
        topic_len = self.sock.read(2)
        maint()
        topic_len = (topic_len[0] << 8) | topic_len[1]
        maint()
        topic = self.sock.read(topic_len)
        maint()
        sz -= topic_len + 2
        if op & 6:
            maint()
            pid = self.sock.read(2)
            pid = pid[0] << 8 | pid[1]
            sz -= 2
        maint()
        msg = self.sock.read(sz)
        maint()
        self.cb(topic, msg)
        maint()
        if op & 6 == 2:
            maint()
            pkt = bytearray(b"\x40\x02\0\0")
            struct.pack_into("!H", pkt, 2, pid)
            self.sock.write(pkt)
        elif op & 6 == 4:
            assert 0

    # Checks whether a pending message from server is available.
    # If not, returns immediately with None. Otherwise, does
    # the same processing as wait_msg.
    def check_msg(self):
        maint()
        self.sock.setblocking(False)
        return self.wait_msg()