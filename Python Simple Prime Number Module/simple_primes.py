#!/usr/bin/python3
from math import sqrt, ceil, log, floor
from secrets import randbelow, randbits


def gcf(a: int, b: int) -> int :
    """
    Find the greatest common factor between two numbers.
    :param a: a natural number
    :param b: a natural number
    :return: a natural GCF
    """
    if b < a :
        a, b = b, a
    while b :
        c = a % b
        a = b
        b = c
    return a


def generate_coprime(x: int, limit: int) -> int :
    """
    Generate a number coprime to x under limit.
    :param x: a natural number greater than 1
    :param limit: a natural number greater than 1
    :return: a natural coprime of x
    """
    while True :
        tmp = randbelow(limit)
        if gcf(x, tmp) == 1 :
            return tmp


def generate_coprimes(x: int, nums: int) -> [int] :
    """
    Return nums numbers coprime to x.
    :param x: a natural number greater than 1
    :param nums: a natural number (greater than 1)
    :return: a set of natural numbers
    """
    tmp = set()
    while len(tmp) < nums :
        tmp.add(generate_coprime(x, x))
    return tmp


def generate_possible_prime_bits(bits: int) -> int :
    """
    Use the "6x +_- 1" trick to generate a possible prime bits bits long.
    :param bits: a natural number greater than 4 (16-on)
    :return: a natural prime candidate
    """
    minimum = 2 ** bits + 1
    maximum = 2 ** (bits + 1) - 2 - minimum
    while True :
        tmp = minimum + randbelow(maximum)
        tmp -= tmp % 6
        tmp += -1 if randbits(1) else 1
        if tmp.bit_length() == bits and tmp > 0 :
            return tmp


def generate_possible_prime_under(limit: int) -> int :
    """
    Use the "6x  +_- 1" trick to generate a possible prime between 1 and limit.
    :param limit: a natural number greater than 4 (16-on)
    :return: a natural prime candidate
    """
    while True :
        tmp = randbelow(limit)
        tmp -= tmp % 6
        tmp += -1 if randbits(1) else 1
        if 0 < tmp < limit :
            return tmp


def crown_jewel_aks_test(x: int, *coprimes: [int]) -> bool :
    """
    Tell if x is a prime via the AKS Test (optimized).
    :param x: a natural prime candidate greater than 2
    :param coprimes: an iterable of tested coprimes
    :return: prime or not
    """
    for y in coprimes :
        if pow(y - 1, x, x) != 0 :
            return False
    return True


def crown_jewel_aks_generated(x: int, nums: int) -> bool :
    """
    Invoke the AKS Test by passing the number x and generating nums coprimes.
    :param x: a natural prime canidate greater than 2
    :param nums: a natural number (greater than 1)
    :return: prime or not
    """
    return crown_jewel_aks_test(x, generate_coprimes(x, nums))


def crown_jewel_brute_force_test(x: int) -> bool :
    """
    Test if x is prime with a brute-force factor search.
    :param x: a natural prime canidate greater than 1
    :return: prime or not
    """
    if x % 2 == 0 : return False
    for y in range(3, int(ceil(sqrt(x)) + 1), 2) :
        if x % y == 0 : return False
    return True


def pnt_calculate(limit: int) -> int :
    """
    Use the PNT (Prime Number Theorem) to estimate how many primes there are between 1 and limit.
    :param limit: a natural number
    :return: a natural number
    """
    return int(floor(limit / log(limit)))


def pnt_calculate_span(lower_limit: int, upper_limit: int) -> int :
    """
    Use the PNT (Prime Number Theorem) to estimate how many primes there are between lower_limit and upper_limit.
    :param lower_limit: a natural number less than upper_limit
    :param upper_limit: a natural number greater than lower_limit
    :return: a natural number
    """
    return pnt_calculate(upper_limit) - pnt_calculate(lower_limit)
