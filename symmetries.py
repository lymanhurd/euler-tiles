# A legal tile must have no blank rows and no blank columns.
def tile_height(tile):
    return len(tile)


def tile_width(tile):
    return len(tile[0])


# List all the possible dihedral symmetries of a tile.
def vflip(tile):
    return tile[::-1]


def hflip(tile):
    return tuple(t[::-1] for t in tile)


def dflip(tile):
    return tuple(''.join(t) for t in zip(*tile))


def symmetries(tile):
    syms = [tile]
    syms += [dflip(t) for t in syms]
    syms += [hflip(t) for t in syms]
    syms += [vflip(t) for t in syms]
    return list(set(syms))
