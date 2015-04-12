# Usage:
#
#  with take_time('description'):
#      func_call()

import contextlib
import time


# Utilities borrowed from Dag
def format_time(t):
    if t > 1 or t == 0:
        units = 's'
    elif t > 1e-3:
        units = 'ms'
        t *= 1e3
    elif t > 1e-6:
        units = 'us'
        t *= 1e6
    else:
        units = 'ns'
        t *= 1e9
    return '%.1f %s' % (t, units)


@contextlib.contextmanager
def take_time(desc):
    t0 = time.time()
    yield
    dt = time.time() - t0
    print '%s took %s' % (desc, format_time(dt))

