#!/usr/bin/env python3

from myeventloop import Log, LOG_DEBUG
from tcpserver import *

Log.set_level(LOG_DEBUG)

# Echoes data when a complete line terminated with \n is detected
class EchoHandler(TCPServerHandler):
    def __init__(self, addr, sock):
        super().__init__(addr, sock)
        self.log_info("Opened")

    def shutdown_callback(self):
        self.log_info("Closed")
        # use default behavior (which is: destroy connection)
        super().shutdown_callback()

    def recv_callback(self, latest):
        self.log_info("Recv ", latest)
        if ord('\n') not in self.recv_buf:
            return

        i = self.recv_buf.index(ord('\n'))
        self.send_buf += "Echoing: ".encode()
        self.send_buf += self.recv_buf[0:i+1]
        self.recv_buf = self.recv_buf[i+1:]
        self.log_info("Echoing")

    # Intercept just for demo logging; use default impl
    def send_callback(self):
        self.log_info("Writing...")
        super().send_callback()

TCPServerEventLoop(("0.0.0.0", 6666), TCPListener, EchoHandler).loop()
