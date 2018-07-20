#!/usr/bin/python3


def better_isqrt(i: int) -> int :  # Vedic Square Root Algorithm
    """
    Implement the Vedic Square Root Algorithm.
    It's slower than math.sqrt(), but it's accurate.
    :param i: whole number
    :return: whole number
    """
    x0 = str(i)
    if len(x0) % 2 : x0 = '0' + x0
    #
    divisor = 0
    dropped = 0
    bases = '0'
    #
    for y0 in range(0, len(x0), 2) :
        dropped = int(str(dropped) + x0[y0 :y0 + 2])
        affixed = 1
        tmp = 0
        while True :
            y1 = (divisor * 10 + affixed) * affixed
            if y1 > dropped :
                affixed -= 1
                y1 = tmp
                break
            affixed += 1
            tmp = y1
        dropped -= y1
        bases += str(affixed)
        divisor = int(bases) * 2
    #
    return int(bases)


LEN = 7
STOP = 1_000

if __name__ == '__main__' :
    print('Started')
    
    with open('test sqrt.txt', 'w+') as of :
        for x in range(STOP) :
            print(str(x) + '\r', end='')  # indicate progress
            #
            a = x ** 2
            b = (x + 1) ** 2
            for y in range(a, b) :
                c = better_isqrt(y)
                d = c * c
                #
                print(
                    str(y).rjust(LEN, '0'),
                    'yields',
                    str(c).rjust(LEN, '0'),
                    ', yielding square',
                    str(d).rjust(LEN, '0'),
                    ', from',
                    str(a).rjust(LEN, '0'),
                    ', to',
                    str(b).rjust(LEN, '0'),
                    end='',
                    file=of)
                #
                if a <= d < b :
                    print(',  fine', file=of)
                else :
                    print(', error', file=of)
                    print('Error')
                    break
    print('\rConcluded'.ljust(len(str(STOP)), ' '))  # indicate conclusion
    
    input('Press [Enter]. ')
