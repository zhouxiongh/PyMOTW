#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Filename:    socketserver_thread.py
# @Author:      jason
# @Time:        2022/1/19 18:49

""" 
Enter module description here
"""
import threading
import socketserver


class ThreadedEchoRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        # Echo the back to the client
        data = self.request.recv(1024)
        cur_thread = threading.currentThread()
        response = b"%s: %s" % (cur_thread.getName().encode(), data)
        self.request.send(response)
        return


class ThreadedEchoServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


if __name__ == "__main__":
    address = ("localhost", 0)  # let the kernel assign a port
    server = ThreadedEchoServer(address, ThreadedEchoRequestHandler)
    ip, port = server.server_address  # what port was assigned?
    print("Server running on ip:{0} port:{1}".format(ip, port))
    server.serve_forever()
