#!/usr/bin/python3.8
from collections import deque
from itertools import count, islice
from io import StringIO
from statistics import mean, variance
from timeit import timeit


primes = deque([2])
times = [0] * (TESTS := 16)

def make_primes():
    n = count(3)
    for i in range(1_0):
        for candidate in n:
            out(candidate)
            if 0 not in (candidate % x for x in primes):
                primes.append(candidate)
                break


def simple_status():
    def simple_status_internal():
        while True:
            tmp = ' ' * int((yield))
            while True:
                new = str(new_raw := (yield))
                if new_raw is None:
                    print(' ' * len(tmp), end = '\r', flush = True)
                    break
                print('\r', new.rjust(len(tmp), ' '), sep = '', end = '', flush = True)
                tmp = new

    next(f := simple_status_internal())
    return lambda msg: f.send(msg)


(out := simple_status())(4)
report = StringIO()
for i in range(TESTS):
    primes.clear()
    times[test_index] = time = timeit(make_primes)
    print(f'test {test_index + 1} time ({time});', file = report)
print('\ntimes', times, 'average', (avg := mean(times)), 'standard deviation', variance(times, avg), file = report)
out(None)
report.seek(0)
print(report.read())
