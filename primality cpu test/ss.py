def simple_status():
    def simple_status_internal():
        while True:
            tmp = ' ' * int((yield))
            while True:
                new = str(new_raw := (yield))
                if new_raw is None:
                    print(' ' * len(tmp), end = '\r', flush = True)
                    break
                print('\r', new.rjust(len(tmp), ' '), sep = '', end = '', flush = True)
                tmp = new

    next(f := simple_status_internal())
    return lambda msg: f.send(msg)

out = simple_status()
for _ in 'ab':
    out(6)  # spaces
    for i in range(1_000_000): out(i)
    for i in range(1_000_000, -1, -1): out(i)
    out(None)
