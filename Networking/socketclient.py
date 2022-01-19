#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Filename:    socketclient.py
# @Author:      jason
# @Time:        2022/1/19 18:57

""" 
Enter module description here
"""
import socket
import argparse

if __name__ == "__main__":
    # Connect to the server
    argparser = argparse.ArgumentParser("Simple TCP client")
    argparser.add_argument("host", help="Server host name")
    argparser.add_argument("port", type=int, help="Server port")
    args = argparser.parse_args()

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((args.host, args.port))

    # Send the data
    message = "Hello, world".encode()
    print("Sending : {!r}".format(message))
    len_sent = s.send(message)

    # Receive a response
    response = s.recv(1024)
    print("Received: {!r}".format(response))
