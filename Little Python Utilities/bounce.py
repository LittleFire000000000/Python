#!/usr/bin/python3


def bounce(modulo: int, here: int, add: int) -> int:  # P()
    # additive version
    # modulo = n > 0, 0 <= here < n, add is any integer
    assert modulo > 0  # line segment AB
    here %= modulo  # point C, 0 <= C < AB
    add = (-1 if add < 0 else 1) * (abs(add) % (2 * modulo))  # trim "add"
    # 0 <= tm <= (AB = modulo)
    modulo_1: int = modulo - 1
    tm: int = here + add
    for _ in '12':
        if tm < 0:  # bounce off A
            tm = tm * -1  # tm | 0 | n : n = 0 - (tm - 0) = -tm
        if tm > modulo_1:  # bounce off B
            # tm | modulo - 1 | n : n = (modulo - 1) - (tm - (modulo - 1)) = 2 * (modulo - 1) - tm
            tm = 2 * modulo_1 - tm
    return tm


def give_positivity(i: int, positive: bool) -> int:  # T()
    return (1 if positive else -1) * abs(i)


def shifted(of_two: int) -> int:
    return 1 << of_two
