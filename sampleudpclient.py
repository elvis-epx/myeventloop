#!/usr/bin/env python3

from myeventloop import Log
from myeventloop.udpserver import *

Log.set_level(Log.DEBUG2)

class EchoEmitterHandler(UDPServerHandler):
    def __init__(self, addr):
        super().__init__(addr, "echo")
        self.counter = 5
        self.task = self.timeout("tsk", 1, self.periodic_send_task)

    def recv_callback(self, addr, dgram):
        self.log_info("Received ", addr, dgram)
        self.counter -= 1
        if self.counter > 0:
            self.task.reset(1)
        else:
            self.destroy()

    def periodic_send_task(self, task):
        dgram = b'abcdefghijklmno'[0:self.counter * 2]
        self.log_info("Sending ", dgram)
        self.sendto(("127.0.0.1", 6666), dgram)
        task.reset(10)

# Port 0 means a random port is assigned by the operating system
EchoEmitterHandler(("0.0.0.0", 0))
UDPServerEventLoop().loop()
