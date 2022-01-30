#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Filename:    ipaddress_interfaces.py
# @Author:      jason
# @Time:        2022/1/19 18:13

""" 
Enter module description here
"""
import ipaddress


ADDRESSES = [
    "10.9.0.6/24",
    "fdfd:87b5:b475:5e3e:b1bc:e121:a8eb:14aa/64",
]


for ip in ADDRESSES:
    iface = ipaddress.ip_interface(ip)
    print("{!r}".format(iface))
    print("network:\n  ", iface.network)
    print("ip:\n  ", iface.ip)
    print("IP with prefixlen:\n  ", iface.with_prefixlen)
    print("netmask:\n  ", iface.with_netmask)
    print("hostmask:\n  ", iface.with_hostmask)
    print()
