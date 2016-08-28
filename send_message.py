#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import sender

if __name__ == '__main__':
    ftype = 'message'
    fid = None
    if len(sys.argv) == 3:
        if sys.argv[1] == '-f':
            ftype = 'fixed'
        elif sys.argv[1] == '-u':
            ftype = 'update'
        fid = sys.argv[2]
    sender.send(ftype, fid, input())
