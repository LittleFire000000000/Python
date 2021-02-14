#!/usr/bin/python3
from math import floor, sqrt

"""Stuff about numbers. Common operations."""


def primitive_period(base: int, modulo: int, remainder: int = 1) -> int:
    """
    For all coprime bases and modulos, base ** power % modulo == remainder.  Find that lowest power.
    WARNING: Ludicrous time complexity
    :param base: natural number
    :param modulo: natural number
    :param remainder: whole number
    :return: lowest power
    """
    if base == modulo:
        return 0
    power_argument: int = 1
    while pow(base, power_argument, modulo) != remainder:
        power_argument += 1
    return power_argument


def gcf(a: int, b: int) -> int:
    """
    Find the greatest common factor/divisor of the integers a and b.
    :param a: whole number
    :param b: natural number
    :return: factor
    """
    if b < a:
        a, b = b, a
    while b:
        c = a % b
        a = b
        b = c
    return a


def is_prime_primitive(x: int) -> bool:
    """
    Test, for sure, if the number x is prime.
    :param x: natural number above 1
    :return: prime or not
    """
    if x < 2:
        return False

    return not any(x % y == 0 for y in range(2, int(floor(sqrt(x)) + 1)))


def factorial_primitive(x: int) -> int:
    """
    For natural number x, return x!.
    :param x: integer
    :return: integer
    """
    result: int = 1
    for y in range(1, x + 1):
        result *= y
    return result


def product(*args: [float]) -> float:
    """
    Find the product of a list of float (or like) objects.
    Return 1.0 with no arguments given.
    :param args: [float] numbers
    :return: float product
    """
    running_product: float = 1.0
    for factor in args:
        running_product *= factor
    return running_product


def product_mean_deviance(*pairs: [(float, float)]) -> (float, float):
    """
    Find the maximum and minimum products of the (mean, abs. deviance) pairs.
    The maximum is given by the product of the means + their deviances.
    The minimum is given by the product of the means - their deviances.
    :param pairs: iterable of float (or like) pairs (tuples are best)
    :return: tuple (maximum, minimum)
    """
    temp_adding_max, temp_subtracting_min = 1.0, 1.0
    for a, b in pairs:
        temp_adding_max, temp_subtracting_min = (a + b) * temp_adding_max, (a - b) * temp_subtracting_min
    return temp_adding_max, temp_subtracting_min


def better_isqrt(i: int) -> int:  # Vedic Square Root Algorithm
    """
    Implement the Vedic Square Root Algorithm.
    It's slower than math.sqrt(), but it's accurate.
    :param i: whole number
    :return: whole number
    """
    x0 = str(i)
    if len(x0) % 2:
        x0 = '0' + x0
    divisor = 0
    dropped = 0
    bases = '0'
    for y0 in range(0, len(x0), 2):
        dropped = int(str(dropped) + x0[y0:y0 + 2])
        affixed = 1
        tmp = 0
        while True:
            y1 = (divisor * 10 + affixed) * affixed
            if y1 > dropped:
                affixed -= 1
                y1 = tmp
                break
            affixed += 1
            tmp = y1
        dropped -= y1
        bases += str(affixed)
        divisor = int(bases) * 2
    return int(bases)


def better_fsqrt(x: int) -> int:
    """
    Implement a fast "bit-squaring" on x.
    :param x: whole number
    :return: whole number
    """
    root_found = 0
    attempt_bit = 1 << (x.bit_length() // 2)
    while attempt_bit:
        new_root = root_found + attempt_bit
        if (x / new_root) < new_root:
            attempt_bit >>= 1
            continue
        root_found = new_root
    return root_found


def better_root(x: int, root: int) -> int:
    """"""
    found_root = 0
    attempt_bit = 1 << (1 + x.bit_length() // root)
    while attempt_bit:
        new_root = found_root + attempt_bit
        if x < new_root ** root:
            attempt_bit >>= 1
            continue
        found_root = new_root
    return found_root


def _test_sqrt(up_to: int, fxn: callable) -> [bool]:
    for i in range(up_to):
        for j in range(i ** 2, (i + 1) ** 2):
            yield fxn(j) == i


def is_sqrt(root_candidate: int, square: int) -> bool:
    """
    Test/verify whether the integral sq. rt. of square is root_candidate.
    >>> root_candidate ** 2 <= square < (root_candidate + 1) ** 2
    :param root_candidate: natural
    :param square: natural
    """
    return root_candidate ** 2 <= square < (root_candidate + 1) ** 2
