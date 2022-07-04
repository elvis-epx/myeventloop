#!/usr/bin/env python3

from myeventloop.myeventloop import EventLoop, Log
from myeventloop.tcpclient import *

Log.set_level(Log.DEBUG2)

# Echoes data when a complete line terminated with \n is detected
class EchoHandler(TCPClientHandler):
    def __init__(self, addr):
        super().__init__(addr)
        self.log_info("Started")
        self.count = 6
        self.conn_timeout = self.timeout("conn_timeout", 5, self.conn_timeout)

    def conn_timeout(self, task):
        self.log_info("Connection failed by timeout")
        self.destroy()

    def connection_callback(self, ok):
        self.conn_timeout.cancel()
        if not ok:
            self.log_info("Connection failed")
            return
        task = self.timeout("send_data", 2, self.send_data)

    def send_data(self, task):
        if self.count <= 0:
            self.destroy()
            return

        self.log_info("Time to send data")
        self.send(("msg%d\n" % self.count).encode())
        self.count -= 1
        task.restart()

    def recv_callback(self, latest):
        self.log_info("Recv ", latest)

    def destroyed_callback(self):
        self.log_info("Bye")

loop = EventLoop()
client = EchoHandler(("127.0.0.1", 6666))
loop.loop()
