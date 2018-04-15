#!/usr/bin/python3
import string

DIGS = string.digits + string.ascii_letters
N_DIGS = len(DIGS)


def int2base(x_int: int, base: int) -> str :
    """
    Produce the digits of the number x in base y.
    :param x_int: a positive integer
    :param base: a natural number
    :return: string of digits
    """
    if x_int < 0 :
        sign = -1
    elif x_int == 0 :
        return DIGS[0]
    else :
        sign = 1
    x_int *= sign
    digits = []
    while x_int :
        digits.append(DIGS[x_int % base])
        x_int //= base
    if sign < 0 :
        digits.append('-')
    digits.reverse()
    return ''.join(digits)


def base2int(x_str: str, base: int) -> int :
    """
    Produce a number from its digits x in base y.
    :param x_str: string of digits
    :param base: a natural number
    :return: the number
    """
    tmp = 0
    for i0, z in enumerate(reversed(list(x_str))) :
        tmp += (base ** i0) * DIGS.index(z)
    return tmp


if __name__ == '__main__' :
    from threading import Thread, Event
    from time import sleep
    
    done = Event()
    
    
    def working() :
        symbols = '|\\-/'
        s_len = len(symbols) - 1
        loc = 0
        while not done.is_set() :
            print('\r' + symbols[loc], end='')
            if loc == s_len :
                loc = 0
            else :
                loc += 1
            sleep(.5)
        print('\r \r', end='', flush=True)
        return
    
    
    def main() :
        show = Thread(target=working, name="PROGRESS", daemon=True)
        show.start()
        discontinue: bool = False
        for x in range(2, 4_000_000) :
            for xb in range(2, N_DIGS + 1) :
                s: str = int2base(x, xb)
                i: int = base2int(s, xb)
                #
                if i != x :
                    print(f'Error: In base {xb}, {x} should be {s}, but iistead resolves to {i}.', flush=True)
                    discontinue = True
                    break
                '''
                else :
                    print(f'Success: In base {xb}, {x} resolves to {s} and reverts back to {i}.', flush=True)
                '''
                del s, i
            if discontinue :
                break
        done.set()
        show.join()
        input('Done. ')
        exit()
    
    
    main()
