from collections import deque
from itertools import count

array = deque()
integers = count(2)
print('Thinking...')
for _ in range(500_000):
    for i in integers:
        if 0 not in (i % j for j in array):
            array.append(i)
            break
print('Writing...')
align = lambda s: str(s).rjust(6, ' ')
with open('primes.txt', 'w', encoding = 'UTF8') as f:
    f.writelines('{}, {};\n'.format(*map(align, iv)) for iv in enumerate(array))
print('Done.')
