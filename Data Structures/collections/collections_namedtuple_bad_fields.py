import collections

try:
    collections.namedtuple('Person', 'name class age')
except ValueError as err:
    print(err)  # ---> Type names and field names cannot be a keyword: 'class'

try:
    collections.namedtuple('Person', 'name age age')
except ValueError as err:
    print(err)  # ---> Encountered duplicate field name: 'age'
