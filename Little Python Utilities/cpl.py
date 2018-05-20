#!/usr/bin/python3
__author__ = 'Aidan'
from sys import argv, stderr
from shutil import copyfile as cp
from os.path import isfile
from py_compile import compile as cpl

class MainClass:
    def load(self):
        if len(argv)==2 and isfile(argv[1]) and argv[1].split('.')[-1]=='py':self.pyf=argv[1]
        else:
            stderr.write('Only takes one .py file.')
            exit(1)
        return self

    def run(self):
        a=cpl(self.pyf)
        a=cp(a,a.replace('__pycache__\\', '').replace('.cpython-36',''))
        print(a)
        return input()

def main():
    global dud; dud=MainClass().load()
    return dud.run()

main();exit()
