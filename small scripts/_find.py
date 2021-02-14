#!/usr/bin/python3
from os import chdir, walk, getcwd
from os.path import isdir, abspath, join
from sys import stderr

def listdir(pt):
    for x,_,z in walk(pt):
        for y in z:
            yield join(x, y)

d0 = getcwd()

try:
    while True:
        d = abspath(input("Path: "))
        if isdir(d):break
    chdir(d)
    while True:
        txt = input('Search for: ')
        if txt.strip() != '':break
    while True:
        caseSence = input("Case sensitive [y/n]: ").strip().lower()
        if caseSence == 'y' or caseSence == 'n':
            caseSence = caseSence == 'y'
            break
    print()
    for a in listdir(d):
        if not isdir(a):
            try:
                with open(a) as b:
                    c = b.read()
                    if c != '':
                        if ((txt.lower() in c.lower()) if not caseSence else (txt in c)):
                            print(a, ' ', end='', sep='')
                            ci = c.find(txt.lower() if not caseSence else txt)
                            c0 = '>> Column {}, Line {}', c.count('\n', 0, ci)
                            c0 = c0[0].format(ci-(c.rfind('\n', 0, ci)), c0[1]+1)
                            print(c0)
                            del c0,ci
                    del c
            except Exception:
                print('Error:', a, file=stderr)
except KeyboardInterrupt:
    print('\nQuit')

input('\n Press enter to exit. ')
    
chdir(d0)
exit()
