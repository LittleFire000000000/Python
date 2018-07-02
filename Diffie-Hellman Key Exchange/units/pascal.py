#!/usr/bin/python3
from sys import stdout

i_row: int

while True :
    try :
        i_row = int(input('What number of rows should the Pascal triangle have? '))
        assert i_row > 0
        break
    except :
        pass

rows: list = [[0, 1, 0]]
max_len: int = 0
max_len_row: int = 0
max_len_row_counter: int = len(str(i_row)) + 1

for a in range(1, i_row) :
    b: list = rows[a - 1]
    shadow: list = [0]
    for x in range(1, len(b)) :
        c: int = b[x] + b[x - 1]
        shadow.append(c)
        if c > max_len : max_len = a
    shadow.append(0)
    rows.append(shadow)

for x in range(i_row) :
    y = ' '.join(str(z).center(max_len) for z in rows[x][1 :-1])
    rows[x] = y
    y = len(y)
    if y > max_len_row : max_len_row = y

for x in range(i_row) :
    rows[x] = str(x + 1).rjust(max_len_row_counter) + ' ' + str.center(rows[x], max_len_row)

file: object

while True :
    file_i = input('Enter destination stream, std_out if inaccessible else a file: ')
    try :
        file = open(file_i, 'w')
        break
    except :
        try :
            file_i = input('Std_out [y] / retry [n]? ')[0]
            assert file_i in 'yYnN'
            if 'y' == file_i.lower() :
                file = None
                break
            else :
                continue
        except :
            print('\a')

print()
for x in rows :
    print(x, file=(stdout if file is None else file), flush=file is None)

if not file is None : file.close()

input('Press <enter> to exit. ')
exit()
