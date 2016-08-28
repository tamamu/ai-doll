#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import threading 
import sender

FID = 'example.timer'
COUNT = 10
INTERVAL = 0.5

def update():
    global COUNT
    COUNT-=1
    if COUNT>0:
        sender.send('update', FID, str(COUNT))
        t=threading.Timer(INTERVAL, update)
        t.start()
    else:
        sender.send('update', FID, "TIME UP")

if __name__ == "__main__":
    if len(sys.argv) == 2:
        COUNT = int(sys.argv[1])
        sender.send('fixed', FID, COUNT)
        t=threading.Timer(INTERVAL, update)
        t.start()
