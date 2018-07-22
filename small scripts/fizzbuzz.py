#!/usr/bin/python3

# Written by Aidan DiPeri
# Explained by Topm Scott @ https://youtu.be/QPZ0pIK_wsc

def play_fizzbuzz(loops: int):
    for i in range(1, loops + 1):
        a, b = (i % 3 == 0), (i % 5 == 0)
        if a: print('Fizz', end='')
        if b: print('Buzz', end='')
        if (not a) and (not b): print(i, end='')
        print()
    return

play_fizzbuzz(100)
input()
exit()
