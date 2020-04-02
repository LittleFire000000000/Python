#!/usr/bin/python3
from enum import IntEnum, unique
from string import digits
from typing import Union

"""Functionalities related to American dollars."""

CM_DIGITS: str = ',' + digits  # [0, 10) and a comma
FREE_PASS: callable = lambda *_: True  #
FREE_DENY: callable = lambda *_: False  #


# Commonwealth

def compound_interest(principle: float, rate: float, compounding: int, time: int) -> float:
    """
    Give the compound interest with the numbers provided.
    :param principle: initial funds
    :param rate: interest rate in percent per period
    :param compounding: number of times compound in a period
    :param time: number of periods
    :return: final funds
    """
    # compound interest p=i(1+r/c)^(tc)
    return principle * (1 + rate / compounding) ** (time * compounding)


def compound_interest2(present_value, annual_rate, periods_per_year, years):
    rate_per_period = annual_rate / periods_per_year
    periods = periods_per_year * years
    return present_value * (1 + rate_per_period) ** periods


def simple_interest(principle: float, rate: float, time: int) -> float:
    """
    Give the compound interest with the numbers provided.
    :param principle: initial funds
    :param rate: interest rate in percent per period
    :param time: number of periods
    :return: final funds
    """
    # p=irt
    return principle * (1 + rate) * time


class IdSmugglerBase:
    """
    Base class of IdSmuggler().
    Made for easy ID generation.
    """
    __id: int

    def __init__(self, starting_point: int = 0):
        """
        Setup this ID slot with the first ID being starting_point.
        :param starting_point: whole number
        """
        self.__id = starting_point

    def get_id(self) -> int:
        """
        Get the next ID pending assignment/ready to use.
        :return: int ID
        """
        return self.__id

    def next_id(self) -> int:
        """
        Get-to-use the next ID pending assignment/ready to use.
        :return: int ID
        """
        tmp: int = self.__id
        self.advance_id()
        return tmp

    def advance_id(self, number_of_times: int = 1):
        """
        Prepare the number_of_times-ahead ID for assignment.
        :param number_of_times: natural number
    """
        self.__id += number_of_times
        return


class IdSmuggler:
    """Issue ID numbers from 0 on easily."""
    MONEY_PARSING_ERRORS = IdSmugglerBase()
    PERCENTAGE_PARSING_ERRORS = IdSmugglerBase()
    MONEY_ACCOUNT_IDS = IdSmugglerBase()
    PRICE_PER_SQUARE_FOOT_PHASES = IdSmugglerBase()
    PROPERTY_IDS = IdSmugglerBase()


# Representations
@unique
class MoneyParsingErrors(IntEnum):
    """Error indicators for is_money()."""
    NO_ERROR = IdSmuggler.MONEY_PARSING_ERRORS.next_id()
    TOO_SHORT = IdSmuggler.MONEY_PARSING_ERRORS.next_id()
    SIGNAGE_MISSING = IdSmuggler.MONEY_PARSING_ERRORS.next_id()
    DOLLAR_SIGN_MISSING = IdSmuggler.MONEY_PARSING_ERRORS.next_id()
    DECIMAL_POINT_MISSING = IdSmuggler.MONEY_PARSING_ERRORS.next_id()
    FIRST_DIGIT_MALFORMED = IdSmuggler.MONEY_PARSING_ERRORS.next_id()
    SECOND_DIGIT_MALFORMED = IdSmuggler.MONEY_PARSING_ERRORS.next_id()
    MISPLACED_COMMA = IdSmuggler.MONEY_PARSING_ERRORS.next_id()
    ABSENT_COMMA = IdSmuggler.MONEY_PARSING_ERRORS.next_id()
    UNRECOGNIZED_DIGIT = IdSmuggler.MONEY_PARSING_ERRORS.next_id()

    @staticmethod
    def is_error(x) -> bool:
        """
        Classify x as indicative of an error or not.
        Integer or float x's are never errors.
        MoneyParsingErrors are always error (except for MoneyParsingErrors.NO_ERROR).
        :param x: int or float or MoneyParsingErrors
        :return: whether error or not
        """
        if isinstance(x, int) or isinstance(x, float):
            return False
        if isinstance(x, MoneyParsingErrors):
            if x == MoneyParsingErrors.NO_ERROR:
                return False
            return True
        return False

    @staticmethod
    def longest() -> int:
        """
        Return the character length of the longest entry.
        Currently, this is equivalent to:
        >>> len('MoneyParsingErrors.SECOND_DIGIT_MALFORMED')
        >>> 41
        :return: int length
        """
        return 41


@unique
class PercentageParsingErrors(IntEnum):
    """ Error indicators for is_percentage()."""
    NO_ERROR = IdSmuggler.PERCENTAGE_PARSING_ERRORS.next_id()
    TOO_SHORT = IdSmuggler.PERCENTAGE_PARSING_ERRORS.next_id()
    SIGNAGE_MISSING = IdSmuggler.PERCENTAGE_PARSING_ERRORS.next_id()
    PERCENT_SIGN_MISSING = IdSmuggler.PERCENTAGE_PARSING_ERRORS.next_id()
    DECIMAL_POINT_MISSING = IdSmuggler.PERCENTAGE_PARSING_ERRORS.next_id()
    MALFORMATION_IN_FLOAT = IdSmuggler.PERCENTAGE_PARSING_ERRORS.next_id()

    @staticmethod
    def is_error(x) -> bool:
        """
        Classify x as indicative of an error or not.
        Integer or float x's are never errors.
        PercentageParsingErrors are always error (except for PercentageParsingErrors.NO_ERROR).
        :param x: int or float or PercentageParsingErrors
        :return: whether error or not
        """
        if isinstance(x, int) or isinstance(x, float):
            return False
        if isinstance(x, PercentageParsingErrors):
            if x == PercentageParsingErrors.NO_ERROR:
                return False
            return True
        return False

    @staticmethod
    def longest() -> int:
        """
        Return the character length of the longest entry.
        Currently, this is equivalent to:
        >>> len('PercentageParsingErrors.DECIMAL_POINT_MISSING')
        >>> 45
        :return: int length
        """
        return 45


def is_money(string: str) -> Union[float, MoneyParsingErrors]:
    """
    Take a formal dollar-value string string and, if possible, return the dollar value in decimal that it represents.
    If not, return MoneyParsingErrors.
    Format description from left to right:
        The format starts with a mandatory signage character (either "+" or "-").
        After that signage character, a mandatory American dollar sign follows ("$").
        After that dollar sign, base ten digits follow.  From right to left, every third digit is followed by a comma.
        After those digits, a decimal point follows.
        After that decimal point, two base ten digits follow.
    Examples include:
    :param string: formal string denoting a dollar amount
    :return: float dollar amount
    """
    temporary: [str] = list(reversed(list(string)))  # reverse string to ease parsing
    if len(temporary) < 6:
        return MoneyParsingErrors.TOO_SHORT  # "+$0.00" has 6 characters
    if temporary[-1] not in ('+', '-'):
        return MoneyParsingErrors.SIGNAGE_MISSING  # verify intact signage
    negative_v: bool = True  # negative until positive
    if temporary.pop(-1) == '+':
        negative_v = False  # if it's positive, it's not negative
    if temporary.pop(-1) != '$':
        return MoneyParsingErrors.DOLLAR_SIGN_MISSING  # require $ after signage
    if temporary[2] != '.':
        return MoneyParsingErrors.DECIMAL_POINT_MISSING  # decimal point after cents
    if not temporary[0] in digits:
        return MoneyParsingErrors.FIRST_DIGIT_MALFORMED  # last digit of cents
    if not temporary[1] in digits:
        return MoneyParsingErrors.SECOND_DIGIT_MALFORMED  # first digit of cents
    cents: str = temporary[1] + temporary[0]  # get cents
    del temporary[0:3]  # clear cents and decimal point to process dollars
    if temporary[0] == ',':  # a comma cannot follow (right to left) the decimal point
        return MoneyParsingErrors.MISPLACED_COMMA  # the comma would be misplace
    place: int = 0  # initiate a parsing cycle for placing commas and digits
    collect_digits: str = ''  # number of dollars
    for character in temporary:  # parse the interim between the "$" and the "."
        if character in CM_DIGITS:  # the character being observed is part of the standard
            if place == 3 and character != ',':  # a comma should be (from right to left) every fourth character
                return MoneyParsingErrors.ABSENT_COMMA  # if a digit is in its place, where is the comma?
            elif place != 3:  # expecting a digit
                if character == ',':  # a comma is where a digit should be
                    return MoneyParsingErrors.MISPLACED_COMMA  # if a comma is in its place, where is the digit?
                collect_digits = character + collect_digits  # extrapolate another digit
            place = (place + 1) % 4  # advance the cycle with 4 characters (3 digits followed by a comma)
        else:  # the observed character isn't part of the standard
            return MoneyParsingErrors.UNRECOGNIZED_DIGIT  # the observed character can't be processed
    balance: float = float(collect_digits + '.' + cents)  # formulate extracted value
    if negative_v:
        balance *= -1  # restore signage
    return balance


def to_money(value: float) -> str:
    """
    Take a dollar amount value and give it as a formal string.
    :param value: float dollar amount
    :return: formal string
    """
    negative: bool = value < 0  # record signage
    temporary: [str, str] = str(round(abs(value), 2)).split('.')  # split input at the decimal point
    counter: int = 0  # offset commas
    temporary_dollars: [str] = list(reversed(temporary[0]))  # prepare to insert commas
    for index in range(3, len(temporary_dollars), 3):  # inserting commas every fourth character
        temporary_dollars.insert(index + counter, ',')  # insert comma with offset
        counter += 1  # update offset
    return ('-' if negative else '+') + '$' + ''.join(reversed(temporary_dollars)) + '.' + temporary[1].ljust(2, '0')


def digits_money(value: float) -> int:
    """
    Give the number of characters value would take if it was a formal string.
    :param value: float dollar amount
    :return: int length
    """
    temporary: int = len(str(round(abs(value), 2)).split('.')[0])
    temporary_comma_count: int = (temporary - 1) // 3  # 0offset
    return 5 + temporary + temporary_comma_count  # 1+- 2$ 5.00


dollars: callable = lambda d: round(d, 2)  # float to dollars


def is_percentage(string: str):
    """
    Take a formal percentage-value string string and, if possible, return the percentage value in decimal that it
    represents.  If not, return PercentageParsingErrors.
    Format description from left to right:
        The format starts with a mandatory signage character (either "+" or "-").
        After that signage character, a normal Python 3 float follows.
        After that float, a mandatory percentage sign follows (%).
    Example include:
    :param string: formal string denoting a percentage amount
    :return: float percentage amount
    """
    if len(string) < 5:
        return PercentageParsingErrors.TOO_SHORT  # +0.0% has 5 characters
    if string[0] not in ('-', '+'):
        return PercentageParsingErrors.SIGNAGE_MISSING
    if string[-1] != '%':
        return PercentageParsingErrors.PERCENT_SIGN_MISSING
    if '.' not in string:
        return PercentageParsingErrors.DECIMAL_POINT_MISSING
    try:
        return (-1 if string[0] == '-' else 1) * float(string[1:-1])
    except IndexError:
        return PercentageParsingErrors.MALFORMATION_IN_FLOAT


def to_percentage(value: float) -> str:
    """
    Take a percentage amount value and give it as a formal string.
    :param value: float percentage amount
    :return: formal string
    """
    return ('-' if value < 0 else '+') + str(abs(value)) + '%'


def digits_percentage(value: float) -> int:
    """
    Give the number of characters value would take if it was a formal string.
    :param value: float percentage amount
    :return: int length
    """
    return 2 + len(str(value))  # 1+- 2% 3float


conversion_m_constant_to_percentage: callable = lambda x: x * 100  # float to percent
conversion_d_percentage_to_constant: callable = lambda x: x / 100  # float from percent


# Classes
class Cycle:
    """Cycle through an iterable."""
    __placeholder: int  # index
    __iterator_current: iter  # iterator from which to draw
    __iterator_raw: iter  # iterator from which to reset

    def _iterate(self, give_stop: bool):
        self.__placeholder += 1
        if self.__placeholder == 0:
            self.__iterator_current = iter(self.__iterator_raw)
        try:
            yield next(self.__iterator_current)
        except StopIteration:
            if give_stop:
                raise
            self.__placeholder = -1
            yield from self._iterate(False)

    def __init__(self, an_iterable: iter):
        """
        Declare a new cycle.
        :param an_iterable: an iterable object
        """
        self.give_iterable(an_iterable)

    # Setup

    def give_iterable(self, iterable: iter):
        """
        Set the cycle with which to operate.
        :param iterable: any iterable
        """
        self.__placeholder = -1
        self.__iterator_raw = iterable
        return

    def retrieve_iterable(self) -> iter:
        """
        Retrieve the cycle with which this generator is operating.
        :return: an iterable
        """
        return self.__iterator_raw

    # Iterate

    def next(self, give_stop: bool = False) -> iter:
        """
        Generator the cycle.
        If give_stop is False, loop to the beginning of the cycle after conclusion,
        If give_stop is True, raise StopIteration at the end of the Cycle, instead of looping.
        :param give_stop: bool stop or loop
        :return: generator
        """
        while True:
            yield next(self._iterate(give_stop))

    def get_iteration(self) -> int:
        """
        What is the index of the item in the cycle currently observed.
        :return: int index
        """
        return self.__placeholder
