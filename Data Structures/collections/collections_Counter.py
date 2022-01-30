#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Filename:    collections_Counter.py
# @Author:      jason
# @Time:        2022/1/30 13:16

""" 
Enter module description here
"""
import collections

# init
print(collections.Counter(["a", "b", "c", "a", "b", "b"]))
print(collections.Counter({"a": 2, "b": 3, "c": 1}))
print(collections.Counter(a=2, b=3, c=1))

# update
c = collections.Counter()
print("Initial :", c)

c.update("abcdaab")
print("Sequence", c)

c.update({"a": 1, "d": 5})
print("Dict     :", c)

# elements
c1 = collections.Counter("extremely")
c1["z"] = 0
print(c1)
print(list(c1.elements()))

# get_values
c2 = collections.Counter("abcdaab")

for letter in "abcde":
    print("{} : {}".format(letter, c2[letter]))

# most_common
print("most_common:", c2.most_common())
