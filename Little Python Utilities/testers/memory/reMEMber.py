#!/usr/bin/python3
from remember import Memory

mem = Memory('', 'mem.txt', str, string_wrap=True)
mem.recall()
print('Last typed: [{}]'.format(mem.get_memories().strip()))
mem.set_memories(input('Type something: '))
mem.remember()
exit()