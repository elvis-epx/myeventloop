#!/usr/bin/env python3

from myeventloop import Log, LOG_DEBUG
from udpserver import *

Log.set_level(LOG_DEBUG)

class EchoHandler(UDPServerHandler):
    def __init__(self, addr):
        super().__init__(addr, "echo")
        self.log_info("Open")

    def recv_callback(self, addr, dgram):
        self.log_info("Recv ", addr, dgram)
        resp = [x for x in dgram]
        resp.reverse()
        self.send_buf.append({'addr': addr, 'dgram': bytearray(resp)})

    # Intercept just for demo logging; use default impl
    def send_callback(self):
        self.log_info("Sending datagam")
        super().send_callback()


EchoHandler(("0.0.0.0", 6666))
UDPServerEventLoop().loop()
