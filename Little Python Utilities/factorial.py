#!/usr/bin/python3
__author__ = 'Aidan'

def factorial(num):
    assert (isinstance(num, int) and num>0), 'Positive integers only.'
    if num==1:return 1
    else:return num*factorial(num-1)
