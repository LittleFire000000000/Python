#!/usr/bin/python3
from os import chdir
from os.path import abspath, isdir, isfile, relpath, samefile
from sys import stderr
from enum import Enum, unique
from tempfile import TemporaryFile
from typing import Dict, Tuple, Callable, List


@unique
class MenuItems(Enum):
    quit = 'q'
    edit_file_selection = 'e'
    menu = 'm'
    set_key = 'k'
    remove_key = 'r'
    remove_all_keys = 's'
    list_keys = 'l'
    replace_in_files = 'f'
    replace_and_remove = 'p'


menu_text: str = 'Actions:\n' + '\n'.join(f'\t{x.name} {x.value}' for x in MenuItems) + '\n-'


def menu():
    print(menu_text)


@unique
class ReplaceMenuItems(Enum):
    find_next = 'fn'
    find_previous = 'fp'
    replace = 'rr'
    replace_all = 'ra'
    replace_all_in_file = 'ri'
    replace_in_all_files = 'rf'
    include = 'i'
    include_all = 'ia'
    include_in_all_files = 'ii'
    include_next = 'in'
    include_previous = 'ip'
    exclude = 'e'
    exclude_all = 'ea'
    exclude_next = 'en'
    exclude_previous = 'ep'
    exclude_in_all_files = 'ei'
    menu_show = 'mm'
    menu_save = 'ms'
    menu_cancel = 'mc'
    menu_cancel_all = 'ml'
    menu_save_and_cancel = 'ma'
    menu_save_and_cancel_all = 'mb'
    menu_stats = 'mt'


@unique
class ReplaceMenuReturn(Enum):
    normal = 'n'
    replace_all_in_file = 'ri'
    replace_in_all_files = 'rf'
    include_in_all_files = 'ii'
    exclude_in_all_files = 'ei'
    menu_cancel_all = 'ml'
    menu_save_and_cancel_all = 'mb'


replace_menu_text: str = 'Replacement options:\n' + '\n'.join(f'\t{x.name} {x.value}' for x in ReplaceMenuItems) + '\n-'


def replace_menu():
    print(replace_menu_text)


dss = Dict[str, str]


class Replacement:
    _rmi: ReplaceMenuItems
    _rmr: ReplaceMenuReturn
    _write_mode: str
    _read_mode: str
    _kvp: dss
    _keys: List[str]
    _total_encountered: int
    _total_replaced: int
    _total_encountered_in_file: int
    _total_replaced_in_file: int
    _files_searched: int
    _total_files_searched: int
    _tmp_file: TemporaryFile

    def __init__(self):
        self._rmi = ReplaceMenuItems.find_previous
        self._rmr = ReplaceMenuReturn.normal
        self._write_mode = 'w'
        self._read_mode = 'r'
        self._kvp = {}
        self._keys = []
        self._total_encountered = 0
        self._total_replaced = 0
        self._total_encountered_in_file = 0
        self._total_replaced_in_file = 0
        self._files_searched = 0
        self._total_files_searched = 0
        self._tmp_file = TemporaryFile(encoding = utf8)

    def __del__(self):
        self._tmp_file.close()

    # Accessors and Modifiers

    @property
    def rmi(self) -> ReplaceMenuItems:
        return self._rmi

    @property
    def rmr(self) -> ReplaceMenuReturn:
        return self._rmr

    @property
    def write_mode(self) -> str:
        return self._write_mode

    @property
    def read_mode(self) -> str:
        return self._read_mode

    @property
    def kvp(self) -> Dict[str, str]:
        return self._kvp

    @property
    def keys(self) -> List[str]:
        return self._keys

    @property
    def total_encountered(self) -> int:
        return self._total_encountered

    @property
    def total_replaced(self) -> int:
        return self._total_replaced

    @property
    def total_encountered_in_file(self) -> int:
        return self._total_encountered_in_file

    @property
    def total_replaced_in_file(self) -> int:
        return self._total_replaced_in_file

    @property
    def files_searched(self) -> int:
        return self._files_searched

    @property
    def total_files_searched(self) -> int:
        return self._total_files_searched

    @property
    def tmp_file(self) -> TemporaryFile:
        return self._tmp_file

    # Actions

    def replace_one(self, file: str):
        ks: List[str] = self._keys
        with open(file, self._read_mode, encoding = utf8) as rf:
            a: str = rf.read()
        tmp_file = self._tmp_file
        tmp_file.seek(0)
        tmp_file.write(a)
        tmp_file.seek(0)
        self._total_encountered_in_file = 0
        self._total_replaced_in_file = 0
        save: bool = True

        def save_it():
            nonlocal file, self, a
            with open(file, self.write_mode, encoding = utf8) as wf:
                wf.write(a)

        while True:
            # todo
            last_hit: int = 0
            line: int = 1
            while True:
                try:
                    inp = ReplaceMenuItems(input('Command> '))
                    break
                except Exception as e:
                    print('prompt eror', e, file = stderr)
                    continue
            if inp == ReplaceMenuItems.find_next:
                pass
            elif inp == ReplaceMenuItems.find_previous:
                pass
            elif inp == ReplaceMenuItems.replace:
                pass
            elif inp == ReplaceMenuItems.replace_all:
                pass
            elif inp == ReplaceMenuItems.replace_all_in_file:
                pass
            elif inp == ReplaceMenuItems.replace_in_all_files:
                pass
            elif inp == ReplaceMenuItems.include:
                pass
            elif inp == ReplaceMenuItems.include_all:
                pass
            elif inp == ReplaceMenuItems.include_in_all_files:
                pass
            elif inp == ReplaceMenuItems.include_next:
                pass
            elif inp == ReplaceMenuItems.include_previous:
                pass
            elif inp == ReplaceMenuItems.exclude:
                pass
            elif inp == ReplaceMenuItems.exclude_all:
                pass
            elif inp == ReplaceMenuItems.exclude_next:
                pass
            elif inp == ReplaceMenuItems.exclude_previous:
                pass
            elif inp == ReplaceMenuItems.exclude_in_all_files:
                pass
            elif inp == ReplaceMenuItems.menu_show:
                replace_menu()
            elif inp == ReplaceMenuItems.menu_save:
                print('Saving... ', end = '')
                save_it()
                print('done.')
            elif inp == ReplaceMenuItems.menu_cancel or inp == ReplaceMenuItems.menu_cancel_all:
                save = False
                break
            elif inp == ReplaceMenuItems.menu_save_and_cancel or inp == ReplaceMenuItems.menu_save_and_cancel_all:
                save = True
                break
            elif inp == ReplaceMenuItems.menu_stats:
                pass
            else:
                print('internal prompt error', file = stderr)
        if save:
            save_it()
        try:
            retn = ReplaceMenuReturn(inp.value)
        except:
            retn = ReplaceMenuReturn.normal
        self._total_encountered += total_encountered
        self._total_replaced_in_file += total_replaced
        self._total_encountered_in_file = total_encountered
        self._total_replaced_in_file = total_replaced
        self._total_files_searched += 1
        self._files_searched += 1


here: str = ''

while True:
    try:
        i = input('Directory> ')
        assert isdir(i), "directory please"
        here = abspath(i)
        chdir(here)
        break
    except Exception as e:
        print('error', e, file = stderr)
        continue

padder: Callable[[int, int], str] = lambda x, p: str(x).rjust(p, '0')
files: [str] = []
rd: dss = {}
utf8: str = 'UTF-8'
print(here)

run: bool = True
while run:
    while True:
        try:
            i = input('File> ')
            assert i.startswith(('+', '-', '.'))
            j, i = i[0], i[1:]
            if j == '.':
                break
            assert isfile(i), 'enter an existing filename'
            i = abspath(i)
        except Exception as e:
            print('file error', e, file = stderr)
            continue
        d: dss = {}
        for f in files:
            try:
                if samefile(f, i):
                    d[f] = relpath(i, here)
                    break
            except Exception as e:
                print('cross-refr. error', e, file = stderr)
        l: bool = len(d) > 0
        try:
            ri = relpath(i, here)
            if j == '-':
                if l:
                    files.remove(ri)
                else:
                    raise AssertionError(f'{repr(i)} not present')
            elif j == '+':
                if l:
                    raise AssertionError(f'{repr(i)} is preset')
                else:
                    files.append(ri)
            else:
                raise AssertionError('internal')
        except AssertionError as e:
            print('assertion error', e, file = stderr)
            continue
        except Exception as e:
            print('j error', e, file = stderr)
            continue

    print('\n'.join(abspath(x) for x in files))

    menu()

    while True:
        i = input('> ')
        try:
            i = MenuItems(i)
        except Exception as e:
            print('input error', e, file = stderr)
            continue
        if i == MenuItems.quit:
            run = False
            break
        elif i == MenuItems.edit_file_selection:
            break
        elif i == MenuItems.menu:
            menu()
        elif i == MenuItems.set_key:
            while True:
                inp = input('Number of lines of key [comma] number of lines of value [0 for 1, 1]: ').lstrip()
                try:
                    if inp.rstrip() in ('', '0'):
                        inp = (1, 1)
                        break
                    zi = inp.index(',')
                    assert zi != -1, "give a comma"
                    inp = [(inp[:zi].strip()), (inp[zi + 1:].strip())]
                    if '0' in inp:
                        inp = None
                        break
                    if inp[0] == '':
                        inp[0] = '1'
                    if inp[1] == '':
                        inp[1] = '1'
                    inp = (int(inp[0], 10), int(inp[1], 10))
                    assert inp[0] >= 1 and inp[1] >= 1, "positive numbers only"
                    break
                except Exception as e:
                    print('number error', e, file = stderr)
                    continue
            if inp is not None:
                pad: int = len(str(max(*inp)))
                key_value: List[str] = ['', '']
                for kv, kvt in ((0, 'key'), (1, 'value')):
                    for i in range(1, inp[kv] + 1):
                        prompt: str = f'[Line {padder(i, pad)} of {kvt}]: '
                        while True:
                            print(prompt, end = '')
                            inp_text: str = input() + '\n'
                            if len(inp_text) > 0 and inp_text[-1] == '\n' and '\n' not in inp_text[:-1]:
                                key_value[kv] += inp_text
                                break
                key, value = key_value[0], key_value[1]
                print(f'Setting key {repr(key)} to value {repr(value)}.')
                rd[key] = value
        elif i == MenuItems.remove_key:
            ask: bool = True
            while ask:
                while True:
                    lines = input('How many lines: ')
                    try:
                        lines = int(lines, 10)
                        assert lines >= 0, "positive"
                        break
                    except Exception as e:
                        print('key-lines error', e, file = stderr)
                        continue
                if lines == 0:
                    break
                key: str = ''
                pad: int = len(str(lines))
                while True:
                    for i in range(1, lines + 1):
                        prompt: str = f'[Line {padder(i, pad)} of the key]: '
                        while True:
                            print(prompt, end = '')
                            inp_text: str = input() + '\n'
                            if len(inp_text) > 0 and inp_text[-1] == '\n' and '\n' not in inp_text[:-1]:
                                key += inp_text
                                break
                    if key in rd:
                        ask = False
                        break
                    else:
                        print('key error', file = stderr)
            if lines > 0:
                print(f'Key {repr(key)}.')
                del rd[key]
        elif i == MenuItems.remove_all_keys:
            rd.clear()
            print('All keys removed.')
        elif i == MenuItems.list_keys:
            print('Keys:\n' + ',\n'.join(f'\t{repr(k)}: {repr(rd[k])}' for k in reversed(sorted(rd.keys()))) + '\n-')
        else:
            if i in (MenuItems.replace_in_files, MenuItems.replace_and_remove):
                replace_menu()
                for file in files:
                    try:
                        pass  # todo use Replacement
                    except Exception as e:
                        print(f'replacement error', e, file = stderr)
                print(
                    f'Of the {total_files1} file{"s" if total_files1 != 1 else ""} queued, {total_files} {"was" if total_files == 1 else "were"} searched, '
                    'and '
                    f'of the {total_encountered} match{"" if total_encountered == 1 else "es"} found, {total_replaced} {"was" if total_replaced == 1 else "were"} replaced.'
                )
                if i == MenuItems.replace_and_remove:
                    rd.clear()
                    print('All keys removed.')
            else:
                print('internal error', file = stderr)

print('Session ended.')
