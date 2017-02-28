__author__ = 'lhurd'


def rotate(t, n):
    return t[n:] + t[:n]


def tiles():
    tile_set = set()
    for i in range(81):
        t = (i % 3, (i / 3) % 3, (i / 9) % 3, (i / 27) % 3)
        t = min([rotate(t, n) for n in (0, 1, 2, 3)])
        tile_set.add(t)
    return tuple(tile_set)
