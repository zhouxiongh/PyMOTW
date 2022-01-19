#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Filename:    server.py
# @Author:      jason
# @Time:        2022/1/19 19:48

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

PORT = 8499
KEY = "foobar!"

import hashlib
import select
import socket
import socketserver
import struct


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


class ThreadingTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


class Socks5Server(socketserver.StreamRequestHandler):
    def handle_tcp(self, sock, remote):
        fdset = [sock, remote]
        while True:
            r, w, e = select.select(fdset, [], [])
            if sock in r:
                if remote.send(self.decrypt(sock.recv(4096))) <= 0:
                    break
            if remote in r:
                if sock.send(self.encrypt(remote.recv(4096))) <= 0:
                    break

    def encrypt(self, data):
        return data.translate(encrypt_table)

    def decrypt(self, data):
        return data.translate(decrypt_table)

    def send_encrpyt(self, sock, data):
        sock.send(self.encrypt(data))

    def handle(self):
        try:
            print("socks connection from ", self.client_address)
            sock = self.connection
            sock.recv(262)
            self.send_encrpyt(sock, "\x05\x00")
            data = self.decrypt(self.rfile.read(4))
            mode = ord(data[1])
            addrtype = ord(data[3])
            if addrtype == 1:
                addr = socket.inet_ntoa(self.decrypt(self.rfile.read(4)))
            elif addrtype == 3:
                addr = self.decrypt(self.rfile.read(ord(self.decrypt(sock.recv(1)))))
            else:
                # not support
                return
            port = struct.unpack(">H", self.decrypt(self.rfile.read(2)))
            reply = "\x05\x00\x00\x01"
            try:
                if mode == 1:
                    remote = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    remote.connect((addr, port[0]))
                    local = remote.getsockname()
                    reply += socket.inet_aton(local[0]) + struct.pack(">H", local[1])
                    print("Tcp connect to", addr, port[0])
                else:
                    reply = "\x05\x07\x00\x01"  # Command not supported
                    print("command not supported")
            except socket.error:
                # Connection refused
                reply = "\x05\x05\x00\x01\x00\x00\x00\x00\x00\x00"
            self.send_encrpyt(sock, reply)
            if reply[1] == "\x00":
                if mode == 1:
                    self.handle_tcp(sock, remote)
        except socket.error:
            print("socket error")


def main():
    server = ThreadingTCPServer(("", PORT), Socks5Server)
    server.allow_reuse_address = True
    print("starting server at port %d ..." % PORT)
    server.serve_forever()


if __name__ == "__main__":
    encrypt_table = "".join(get_table(KEY))
    decrypt_table = str.maketrans(encrypt_table, "")
    main()
