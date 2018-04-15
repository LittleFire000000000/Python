#!/usr/bin/python3
__author__ = 'Aidan'


def switch(*a, default=None, error=None):
    global length
    length = len(a)
    if (length-1) % 3 == 0:
        for n, b in enumerate(a):
            if (n-1) % 3 == 0:
                if a[0] == a[n]:
                    del length
                    try:
                        return a[n+1](a[n+2])
                    except TypeError:
                        try:
                            return a[n+1]()
                        except TypeError:
                            return a[n+1]
        if default is not None:
            default[0](default[1])
    else:
        if default is not None:
            default[0](default[1])
        if error is not None:
            error[0](error[1])
    del length
    return None
