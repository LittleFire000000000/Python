#!/usr/bin/python3.8
from collections import deque
from itertools import count, islice, starmap
from statistics import mean, variance
from timeit import timeit

TESTS = 16
ps = deque()
ts = [0] * TESTS


@timeit
def make_primes():
    ps.clear()
    ps.extend(islice((x for x in count(2) if 0 not in (x % y for y in ps)), 1_000))


def record(test_index: int) -> str:
    ts[test_index] = time = make_primes()
    return f'test {test_index + 1} time ({time});'


print(*map(record, range(TESTS)), '', sep = '\n')
print('times', ts, 'average', (avg := mean(ts)), 'standard deviation', variance(ts, avg))

