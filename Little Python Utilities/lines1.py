#!/usr/bin/python3
from os import walk
from os.path import isdir, isfile, join, abspath
from typing import Tuple


gf_exclude: Tuple = ('__pycache__', '.idea')


def gen_filenames(path: str) -> [str]:
    for directory, _, filenames in walk(path):
        if any(x in directory for x in gf_exclude):
            continue
        for _filename in filenames:
            yield join(directory, _filename)


def report(_filename: str) -> Tuple[int, int]:
    print(f'"{_filename}" ', end = '')
    try:
        file = open(_filename, 'r', encoding = 'UTF-8')
    except PermissionError:
        print('Gave permission error')
        raise
    _lines: int = 0
    _characters: int = 0
    try:
        for line in file.readlines():
            _lines += 1
            _characters += len(line)
    except UnicodeDecodeError:
        print('Gave unicode error')
        raise
    finally:
        file.close()
    print(
        f'Has {_lines} line{"s" if _lines != 1 else ""} and {_characters} character{"s" if _lines != 1 else ""} in it.')
    return _lines, _characters


u_in: str
file_not_dir: bool

while True:
    u_in = input('File or folder: ')
    file_not_dir = isfile(u_in)
    if file_not_dir:
        break
    elif isdir(u_in):
        file_not_dir = False
        break

if file_not_dir:
    try:
        report(u_in)
    except PermissionError:
        pass
else:
    lines: int = 0
    characters: int = 0
    files_seen: int = 0
    files_reported: int = 0
    for filename in gen_filenames(u_in):
        files_seen += 1
        try:
            l, c = report(filename)
            files_reported += 1
            lines += l
            characters += c
        except (PermissionError, UnicodeDecodeError):
            pass
    print(
        f'In total, {files_seen} file{"s" if files_seen != 1 else ""} were detected and '
        f'{files_reported} thereof {"were" if files_reported != 1 else "was"} examined.\n'
        f'A total of {str(lines) + " lines" if lines != 1 else "1 line"} and '
        f'{str(characters) + " characters" if characters != 1 else "1 character"} '
        f'were detected')

input(
    f'"{abspath(u_in)}"\n'
    'Hit [Enter]. ')

