from os import listdir, environ
from os.path import isfile, isdir, join

a,b = environ['path'], environ['PATHEXT']
if None in (a,b):exit()

a,b = a.split(';'), b.split(';')
c = list()

for w in a:
	for d,f in environ.items(): w = w.replace('%'+d+'%', f)
	if isdir(w):
		d = tuple(n for n in listdir(w) if isfile(join(w, n)))
		for x in d:
			for y in b:
				if x.lower().endswith(y.lower()):
					z = join(w, x)
					c.append(list((('.'.join(z.split('\\')[-1].split('.')[:-1]), y, '\\'.join(z.split('\\')[:-1])))))
					del z
					break
		del d

if len(c) != 0:
	for x in range(len(c)): c[x].reverse()
	c.sort()

	h = max((len(x[0]) for x in c))+1
	i = max((len(x[1]) for x in c))+1
	j = max((len(x[2]) for x in c))+1

	for x in range(len(c)):
		c[x][0] = c[x][0].ljust(h)
		c[x][1] = c[x][1].ljust(i)
		c[x][2] = c[x][2].ljust(j)

	for x in range(len(c)): c[x].reverse()
	for x in range(len(c)): print(''.join(c[x]))

del a,b,c,h,i,j

input('\nPress enter to exit.')
exit()
