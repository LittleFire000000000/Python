#!/usr/bin/python3
from math import sqrt, floor

"""
Stuff about numbers.
Common operations.
"""


def primitive_period(base: int, modulo: int, remainder: int = 1) -> int :
    """
    For all coprime bases and modulos, base ** power % modulo == remainder.  Find that lowest power.
    WARNING: Ludicrous time complexity
    :param base: natural number
    :param modulo: natural number
    :param remainder: whole number
    :return: lowest power
    """
    if base == modulo : return 0
    power_argument: int = 1
    while pow(base, power_argument, modulo) != remainder : power_argument += 1
    return power_argument


def gcf(a: int, b: int) -> int :
    """
    Find the greatest common factor/divisor of the integers a and b.
    :param a: whole number
    :param b: natural number
    :return: factor
    """
    if b < a : a, b = b, a
    while b :
        c = a % b
        a = b
        b = c
    return a


def is_prime_primitive(x: int) -> bool :
    """
    Test, for sure, if the number x is prime.
    :param x: natural number above 1
    :return: prime or not
    """
    if x < 2 : return False
    for y in range(2, int(floor(sqrt(x)) + 1)) :
        if x % y == 0 : return False
    return True


def factorial_primitive(x: int) -> int :
    """
    For natural number x, return x!.
    :param x: integer
    :return: integer
    """
    result: int = 1
    for y in range(1, x + 1) : result *= y
    return result


def product(*args: [float]) -> float :
    """
    Find the product of a list of float (or like) objects.
    Return 1.0 with no arguments given.
    :param args: [float] numbers
    :return: float product
    """
    running_product: float = 1.0
    for factor in args : running_product *= factor
    return running_product


def product_mean_deviance(*pairs: [(float, float)]) -> (float, float) :
    """
    Find the maximum and minimum products of the (mean, abs. deviance) pairs.
    The maximum is given by the product of the means + their deviances.
    The minimum is given by the product of the means - their deviances.
    :param pairs: iterable of float (or like) pairs (tuples are best)
    :return: tuple (maximum, minimum)
    """
    temp_adding_max, temp_subtracting_min = 1.0, 1.0
    for a, b in pairs :
        temp_adding_max, temp_subtracting_min = (a + b) * temp_adding_max, (a - b) * temp_subtracting_min
    return temp_adding_max, temp_subtracting_min
