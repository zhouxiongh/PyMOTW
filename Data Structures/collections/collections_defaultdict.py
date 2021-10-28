import collections


def default_factory():
    return 'default value'


d = collections.defaultdict(default_factory, foo='bar')
print('d:', d)
print('foo =>', d['foo'])
print('bar =>', d['bar'])

# two dimensional dict
d = collections.defaultdict(dict)
d['a']['b'] = 1
print("a in d", 'a' in d)
print("b in d", 'b' in d)
