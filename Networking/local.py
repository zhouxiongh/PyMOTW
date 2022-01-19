#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Filename:    local.py
# @Author:      jason
# @Time:        2022/1/19 19:47

""" 
Enter module description here
"""
#!/usr/bin/env python

# Copyright (c) 2012 clowwindy
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

SERVER = "myserver_ip_or_hostname"
REMOTE_PORT = 8499
PORT = 1080
KEY = "foobar!"

import hashlib
import select
import socket
import socketserver
import struct
import threading
import time


def get_table(key):
    # m = hashlib.md5.new()
    m = hashlib.md5()
    m.update(key.encode())
    s = m.digest()
    (a, b) = struct.unpack("<QQ", s)
    table = [c for c in str.maketrans("", "")]
    for i in range(1, 1024):
        table.sort(key=lambda x, y: int(a % (ord(x) + i) - a % (ord(y) + i)))
    return table


encrypt_table = "".join(get_table(KEY))
decrypt_table = str.maketrans(encrypt_table, "")

my_lock = threading.Lock()


def lock_print(msg):
    my_lock.acquire()
    try:
        print("[%s]%s" % (time.ctime(), msg))
    finally:
        my_lock.release()


class ThreadingTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


class Socks5Server(socketserver.StreamRequestHandler):
    def encrypt(self, data):
        return data.translate(encrypt_table)

    def decrypt(self, data):
        return data.translate(decrypt_table)

    def handle_tcp(self, sock, remote):
        fdset = [sock, remote]
        counter = 0
        while True:
            r, w, e = select.select(fdset, [], [])
            if sock in r:
                r_data = sock.recv(4096)
                if counter == 1:
                    try:
                        lock_print("Connecting " + r_data[5 : 5 + ord(r_data[4])])
                    except Exception:
                        pass
                if counter < 2:
                    counter += 1
                if remote.send(self.encrypt(r_data)) <= 0:
                    break
            if remote in r:
                if sock.send(self.decrypt(remote.recv(4096))) <= 0:
                    break

    def handle(self):
        try:
            sock = self.connection
            remote = socket.socket()
            remote.connect((SERVER, REMOTE_PORT))
            self.handle_tcp(sock, remote)
        except socket.error:
            lock_print("socket error")


def main():
    print("Starting proxy at port %d" % PORT)
    server = ThreadingTCPServer(("", PORT), Socks5Server)
    server.serve_forever()


if __name__ == "__main__":
    main()
