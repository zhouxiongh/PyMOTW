import hashlib
import time

data = open(__file__, 'rb').read()

loop_start = time.perf_counter()

for i in range(5):
    iter_start = time.perf_counter()
    h = hashlib.sha1()
    for i in range(300000):
        h.update(data)
    chsum = h.digest()
    now = time.perf_counter()
    loop_elpased = now - loop_start
    iter_elpased = now - iter_start
    print(time.ctime(), ': {:0.3f} {:0.3f}'.format(iter_elpased, loop_elpased))