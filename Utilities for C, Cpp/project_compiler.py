#!/usr/bin/python3
from os import chdir, getcwd, walk
from os.path import join, getsize
from subprocess import Popen, PIPE
from colorama import *
from sys import argv

original_dir = '\\'.join(argv[0].split('\\')[:-1])
RESET = Fore.GREEN+Style.BRIGHT
chdir(original_dir)
init()

def end(code):
    print(RESET+'Press enter to exit. '+Style.RESET_ALL, end='')
    deinit()
    chdir(original_dir)
    input()
    exit(code)

def cmd_args(s):
    return ''.join((a if a not in '^<>"|%' else '^'+a) for a in s)

def represent_dir(a=None, error=False):
    s = original_dir if a is None else a
    for b in (original_dir, original_dir2):
        s = s.replace(b, Fore.BLUE+'<original_dir>'+(RESET if not error else Fore.RED+Style.BRIGHT))
    return s

def safe_print(a):
    if a[0] != '':print(a[0])
    if a[1] != '':print(a[1])
    return None

def namer():
    global name, name0
    name0 = input('Name.exe: ')
    name = cmd_args(name0)
    name  = name  if name  != '' else cmd_args(('Debug' if debug else '')+getcwd().split('\\')[-1])
    name0 = name0 if name0 != '' else          ('Debug' if debug else '')+getcwd().split('\\')[-1]
    if not name0.endswith('.exe'):name0 += '.exe'
    if not name .endswith('.exe'):name  += '.exe'
    print('\t'+'Final: '+Fore.YELLOW+'"'+RESET+name+Fore.YELLOW+'"'+RESET+'\n')
    return None

def main():
    file_.clear()
    for a in files:
        d = a.split('.')[-1].lower() != 'rc'
        b = '.'.join(cmd_args(a).split('.')[:-1]) + ('.o' if d else '.res')
        file_.append(b)
        
        cmd = ('mingw32-g++ -Wall -fexceptions -{} {}-o "{}" -c "{}"{}'.format(('g' if debug else 'O2'), cpp11, cmd_args(b), cmd_args(a), head0)
               if d else
               'windres -J rc -O coff -i "{}" -o "{}"{}'.format(cmd_args(a), cmd_args(b), head0))
        print(represent_dir(cmd), '\n'+Fore.RED+Style.BRIGHT)
        cmd = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
        cmd0 = cmd.communicate()
        cmd0 = tuple(represent_dir(a.decode(), True) for a in cmd0)
        safe_print(cmd0)
        print(RESET, end='')
        if cmd.returncode != 0:end(1)

    cmd = 'mingw32-g++ -o "{}\\{}" {}{}{}'.format(original_dir2, name, ' '.join('"{}"'.format(cmd_args(a)) for a in file_), ('' if debug else ' -s'), head1)
    print(represent_dir(cmd), '\n'+Fore.RED+Style.BRIGHT)
    cmd = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
    cmd0 = cmd.communicate()
    cmd0 = tuple(represent_dir(a.decode(), True) for a in cmd0)
    safe_print(cmd0)
    if cmd.returncode != 0:end(1)

    print('\n{}{}{} Has {} Ones and Zeros!\n'.format(Fore.YELLOW+'"'+RESET, name0, Fore.YELLOW+'"'+RESET, getsize(name0)*8))
    return None
    

print(RESET+'This utility was created by Aidan I DiPeri for compiling C++. Copyright Aidan, 2015.\n')

while True:
    cpp11 = input('Use C++ 11 [y,l / n,0]: ').lower().strip()
    if cpp11 == '':cpp11 = ' '
    if cpp11 in 'y1n0':
        cpp11 = '--std=c++11 ' if cpp11 in 'y1' else ''
        break
    else:print('\a', end='')

while True:
    debug = input('Debug mode [y,n, both]: ').lower().strip()
    if debug == '':debug = ' '
    if debug in 'ynb':
        debug = (True, False, None)['ynb'.index(debug)]
        break
    else:print('\a', end='')

original_dir2 = cmd_args(original_dir)
    
files = list(((a, b) for a, _, b in walk(original_dir)))
file_ = []
for a, b in files:
    for c in b:
        file_.append(join(a, c))
files = tuple(a for a in file_ if a.split('.')[-1].lower() in ('c', 'cpp', 'cxx', 'f', 'rc'))
file_ = []
for a in files:
    b = '\\'.join(a.split('\\')[:-1])
    if b not in file_:file_.append(b)
    
head0 = ''
for b in file_:head0 += ' "-I{}"'.format(cmd_args(b))
head1 = ''
for b in file_:head1 += ' "-L{}"'.format(cmd_args(b))
file_ = []

if debug != None:
    namer()
    main()
else:
    for a_ in (True, False):
        debug = a_
        namer()
        main()

end(0)
