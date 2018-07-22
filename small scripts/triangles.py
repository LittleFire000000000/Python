#!/usr/bin/python3
from math import sqrt
while True:
    try:
        a = input("A ")
        b = input("B ")
        c = input("C ")
        
        if a=="":print("A is \|(c**2-b**2),", sqrt(float(c)**2-float(b)**2))
        if b=="":print("B is \|(c**2-a**2),", sqrt(float(c)**2-float(a)**2))
        if c=="":print("C is \|(a**2+b**2),", sqrt(float(a)**2+float(b)**2))
    except:print("Error")
