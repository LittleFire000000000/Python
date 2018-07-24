#!/usr/bin/python3
from math import log10
from random import randrange, seed
from sys import maxsize

"""
Utility functions.
"""


def file_named(file: int = 0) -> str :
    """
    Return ".out.txt" if file == 0 else ".out(file).txt".
    :param file: whole number
    :return:  file name
    """
    return '.out.txt' if file == 0 else f'.out{file}.txt'


def output(mode: str = 'r', file: int = 0) -> open :
    """
    Open ".out.txt" if file == 0 else ".out(file).txt", in mode mode+.
    :param mode: file mode
    :param file: whole number
    :return: file handle
    """
    return open(file_named(file), mode + '+', encoding='utf-8')


def output_entries(file: open, how_many: int) :
    """
    Make a note that how_many entry(s) will exist in file file.
    :param file: file handle
    :param how_many: number of entries
    :return:
    """
    out_write_lines(file, f'Here are {how_many} entries.\n')


def mark_file_help(file: open, note_text: str = "No documentation specified.", new_line: bool = True) :
    """
    Add a helpful note to contextualise the data in file file (and an empty line thereafter if new_line).
    :param file: file handle
    :param note_text: string of documentation
    :param new_line: whether to add a new line
    :return:
    """
    out_write_line(file, note_text, new_lines=new_line)


def out_write_lines(file: open, *lines: [str], new_lines: bool = True) :
    """
    Write multiple lines lines to file file, delineated by new-line characters if new_lines.
    :param file: file handle
    :param lines: lines of text
    :param new_lines: whether to delineate
    :return:
    """
    if new_lines :
        file.writelines(x + '\n' for x in lines)
    else :
        file.writelines(x for x in lines)


def out_write_line(file: open, line: str, *objects: [object], new_lines: bool = True) :
    """
    Write a line to file file.  If line is a format string, objects is its list of plug-in values.
    If new_lines, delineate the lines with new-line characters.
    :param file: file handle
    :param line: text or format-string
    :param objects: plug-in values
    :param new_lines: whether to delineate
    :return:
    """
    tmp: str = ('\n' if new_lines else '')
    if len(objects) :
        file.writelines((line.format(*objects) + tmp,))
    else :
        file.writelines((line + tmp,))


def out_sort(sort: bool = True, reverse: bool = False, number_entries: int = None, file: int = 0) :
    """
    Open .out(file).txt, sort its lines if sort, reversed in order if reverse, and\
    insert a line-count if number_entries is None else number_entries.
    WARNING: .out(file).txt shouldn't be open.
    :param sort: whether to sort its lines.
    :param reverse: sorting order
    :param number_entries: optional entry/projected-count
    :param file: whole number
    :return:
    """
    with output('r', file) as inf :
        tmp: [str] = inf.readlines()
    if sort : tmp.sort(reverse=reverse)
    with output('w', file) as of :
        if number_entries is None :
            output_entries(of, len(tmp))
        elif isinstance(number_entries, int) :
            if number_entries >= 0 : output_entries(of, number_entries)
        of.writelines(tmp)


def get_input(x: int = 0, prompt: str = 'Number of entries', input_processor: callable = int) -> int :
    """
    Get an integral number from console, offset by x, giving the text prompt prompt. Prompt should omit its collin.
    The input_processor takes the raw input and converts it into something useful (int by default).
    :param x: offset
    :param prompt: string
    :param input_processor: callable object
    :return: integer (by default)
    """
    prompt += ': '
    while True :
        try :
            i_value: int = input_processor(input(prompt))
            assert i_value > 0
            return i_value + x
        except :
            pass


def is_within_bounds(candidate: int, minimum: int = None, maximum: int = None) -> bool :
    """
    Give whether a candidate is within an interval.
    The interval [minimum, maximum] of integers are accepted.
    A minimum of None represents -infinity as the minimum.
    A maximum of None represents +infinity as the maximum.
    :param candidate: int proposed
    :param minimum: lower bound
    :param maximum: upper bound
    :return: bool candidate within interval
    """
    try :
        if minimum is not None : assert candidate >= minimum
        if maximum is not None : assert candidate <= maximum
        return True
    except :
        return False


def get_input_advanced(prompt: str = "Number of entries", minimum: int = 0, maximum: int = None,
                       input_processor: callable = int) -> int :
    """
    Get an integer from the console, with the prompt prompt. Prompt should omit its collin.
    The interval [minimum, maximum] of integers are accepted.
    A minimum of None represents -infinity as the minimum.
    A maximum of None represents +infinity as the maximum.
    The input_processor takes the raw input and converts it into something useful (int by default).
    :param prompt: string
    :param minimum: integer or None
    :param maximum: integer or None
    :param input_processor: callable object
    :return: integer (by default)
    """
    prompt += ': '
    while True :
        try :
            i_value: int = input_processor(input(prompt))
        except :
            continue
        if is_within_bounds(i_value, minimum, maximum) :
            return i_value


def get_seed(prompt: str = 'Seed', minimum: int = 0, maximum: int = None) -> int :
    """
    Get an integer from the console, with the prompt prompt. Prompt should omit its collin.
    If the integer is zero, random.seed() is reseeded randomly.
    If the integer is above zero, random.seed() is reseeded with the integer.
    The interval [minimum, maximum] of integers are accepted.
    A minimum of None represents 0 as the minimum.
    A maximum of None represents sys.maxsize as the maximum.
    :param prompt: string
    :param minimum: whole number or None
    :param maximum: whole number or None
    :return: integer
    """
    prompt += ': '
    while True :
        try :
            i_value = int(input(prompt))
            assert is_within_bounds(i_value, minimum, maximum)
            assert 0 <= i_value <= maxsize
            break
        except :
            pass
    #
    i_value = abs(i_value)
    if i_value == 0 :
        i_value = randrange(maxsize)
    seed(i_value)
    return i_value


def stop(message: str = "Done", end: bool = True) :
    """
    Acknowledge program conclusion with user.
    If end, call exit().
    :param message: text to accompany the indication
    :param end: whether to call exit()
    :return:
    """
    input(message + '. ')
    if end : exit()


def get_pad_length(v: int) -> int :
    """
    In base 10, determine the number of digits the integer v has.
    :param v: integer
    :return: its length
    """
    return len(str(v))


get_pad_length_int: callable(int) = lambda x : int(log10(x)) + 1
get_pad_length_abs: callable(int) = lambda x : int(log10(abs(x))) + 1


def get_pad_lengths_float(x: float) -> (int, int) :
    """
    For a floating point number x, return the length of its floor and then its decimal part.
    :param x: a float
    :return: (floor length, decimal length)
    """
    tmp: (str, str) = str(x).split('.')
    return len(tmp[0]), len(tmp[1])


def pad_value_int(value: int, pad: int, pad_char: str = ' ') -> str :
    """
    Right-justify the string of the integer value to pad-characters with the ch. pad_char.
    :param value: integer
    :param pad: length
    :param pad_char: padding
    :return: string
    """
    return str(value).rjust(pad, pad_char)


def pad_value_float(value: float, pad_int: int, pad_decimal: int, pad_char: str = ' ') -> str :
    """
    Right-justify the string of the float value's floor to pad_int-characters with the ch. pad_char;
    Left justify, after the decimal-point, the decimal pad_decimal-characters with 0.
    :param value: float
    :param pad_int: floor length
    :param pad_decimal: decimal part length
    :param pad_char: padding
    :return: string
    """
    t: [str] = str(value).split('.')
    return t[0].rjust(pad_int, pad_char) + '.' + t[1].ljust(pad_decimal, '0')


def int_suffix(x: int) -> str :
    """
    With position x in a series, determine, in English, its suffix.
    :param x: element
    :return: string/suffix
    """
    tmp: str = str(x)
    if tmp.endswith('11') or tmp.endswith('12') or tmp.endswith('13') :
        return 'th'
    elif tmp.endswith('1') :
        return 'st'
    elif tmp.endswith('2') :
        return 'nd'
    elif tmp.endswith('3') :
        return 'rd'
    else :
        return 'th'
