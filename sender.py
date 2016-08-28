# -*- coding: utf-8 -*-
import socket

FORMAT = """
{"type": "%s", "id": "%s", "data": "%s"}
"""

def send(ftype, fid, text, host='localhost', port=45912):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto((FORMAT % (ftype, fid, text)).encode('utf-8'), (host, port))

