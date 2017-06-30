#!/usr/bin/python3
from sys import argv
from time import sleep
from os.path import isfile

fname = ''
if len(argv)>1:
    if isfile(  argv[1]):
        fname = argv[1]

while True:
    print()
    if not fname:
        while True:
            fname = input('File: ')
            if isfile(fname):
                print()
                break
            elif not fname: break
            print('\a', end='')
    else:
        print('File: '+fname, end='\n\n')

    if not fname: break

    try:
        with open(fname) as f:
            a = list(list(y[:-1].split(' // ')) for y in f.readlines() if '); // ' in y).copy()
            # align header components
            
            z = 0
            for x,y in a:
                tmp = x
                while tmp.find('  ') != -1:
                    tmp = tmp.replace('  ', ' ')
                a[z][0] = tmp.strip()
                z += 1

            ReturnTypes = []
            Names = []
            Types = []
            Variables = []

            for func,_ in a:
                rti = func.find(' ')
                ReturnTypes.append(func[:rti])
                nmi = func.find('(')
                Names.append(func[rti+1:nmi])
                nmi0 = func.find(')')
                args = func[nmi+1:nmi0]

                tmp0 = len(Variables)
                Variables.append([])
                Types.append([])

                if ',' in args:
                    args = tuple(t.strip() for t in args.split(','))
                    for c in args:
                        if ' ' in c:
                            d = c.split('=')[0].split(' ')
                            Types[tmp0].append(d[0])
                            Variables[tmp0].append(d[1])
                        else:
                            Types[tmp0].append(c.split('=')[0])
                            Variables[tmp0].append('')
                else:
                    if ' ' not in args:
                        Types[tmp0].append(args.split('=')[0])
                        Variables[tmp0].append('')
                    else:
                        d = args.split('=')[0].split(' ')
                        Types[tmp0].append(d[0])
                        Variables[tmp0].append(d[1])

            ReturnType0 = max(len(x) for x in ReturnTypes)
            Name0       = max(len(x) for x in Names      )
            Type0       = max(len(y) for x in Types       for y in x)
            Variable0   = max(len(y) for x in Variables   for y in x)

            Array = []
            Parentheses = 0

            for x in range(len(a)):
                s = list((ReturnTypes[x].ljust(ReturnType0), '  '))
                s.append(Names[x].ljust(Name0))

                p = ''
                var = Variables[x]
                typ = Types[x]
                if len(typ):
                    p = ', '.join(' '.join((typ[y].ljust(Type0), var[y].ljust(Variable0))) for y in range(len(typ)))
                    if len(p) > Parentheses: Parentheses = len(p)
                s.append(p)

                Array.append(s)

            for x in range(len(a)):
                Array[x] = ''.join((Array[x][0], Array[x][1], Array[x][2], ' ( ', Array[x][3].ljust(Parentheses), ' ) ;'))
                a[x][0] = Array[x]

            #
            for y in range(len(a)): a[y] = list(reversed(a[y]))
            b = (max(len(y) for y,_ in a)+1, max(len(y) for _,y in a))
            for y in range(len(a)):
                a[y][0] = a[y][0].ljust(b[0], '_')
                a[y][1] = a[y][1].rjust(b[1])
            bar = "-"*(sum(b)+6)
            print("{} Functions:\n{}\n{}\n{}\n".format(len(a), '\t+'+bar+'+', '\n'.join(('\t| '+' :: '.join(y)+' |') for y in a),
                                                               '\t+'+bar+'+'))
    except:
        print('Couldn\'t read file.')

    fname = ''
    input('--')

print('Bye. ', end='', flush=True)
sleep(3)
