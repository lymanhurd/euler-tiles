from __future__ import print_function

__author__ = 'lhurd'

import logging

import tile_solver.tile
from dancing_links.links import make_objects, search


# Returns a tuple consisting of a tile rotated by 0, 180 degrees.
def rot2(tile):
    return tuple([tile[i:] + tile[:i] for i in (0, 2)])


# Returns a tuple consisting of a tile rotated by 0, 90, 180, 270 degrees.
def rot4(tile):
    return tuple([tile[i:] + tile[:i] for i in (0, 2, 4, 6)])


# The sides are enumerated clockwise: (top. right, bottom, left) where
# (1, 0) means black, and (0, 1) white.
corner = (1, 0, 1, 0, 0, 1, 0, 1)  # (B, B, W, W)
end = (1, 0, 0, 1, 0, 1, 0, 1)  # (B, W, W, W)
straight = (1, 0, 0, 1, 1, 0, 0, 1)  # (B, W, B, W)
# The tee stands in for the TEE shape as well as the ASYMMETRICAL shape.
tee = (1, 0, 1, 0, 1, 0, 0, 1)  # (B, B, B, W)
# The cross takes the place of the CROSS and the STRIPES.
cross = (1, 0, 1, 0, 1, 0, 1, 0)  # (B, B, B, B)

corners = rot4(corner)
ends = rot4(end)
straights = rot2(straight)
tees = rot4(tee)
crosses = (cross,)


# There are 4 corners, 4 ends, 1 straight, 4 tees, 3 crosses in the tile set.
d8tiles = ((corners,) * 4 + (ends,) * 4 + (straights,) + (tees,) * 4 +
           (crosses,) * 3)


# The matrix has NUM_TILES columns indicating the piece and
# 8 * WIDTH * HEIGHT columns indicating legal placements.
def tile_rows8(tile, tile_number, num_tiles=16, width=4, height=4):
    """Return the rows for a given tile in a given orientation.

    Args:
        tile: 8-tuple representing the tile.
        tile_number: the tile index for this tile.

    Returns:
        List of rows to the matrix contributed by this tile (in this
        orientation).
    """
    prefix = [0] * num_tiles
    prefix[tile_number] = 1
    rows = []
    for pos in range(width * height):
        # Eliminate tiles that would protrude towards the top or left edge.
        if pos / width == 0 and tile[0] == 1:  # top is black
            continue
        if pos % width == 0 and tile[6] == 1:  # left is black
            continue
        row = prefix + shorten((pos * 8 * [0]) + list(tile) +
                               (width * height - pos - 1) * 8 * [0])
        rows.append(prefix + (pos * 8 * [0]) + list(tile) +
                    (width * height - pos - 1) * 8 * [0])
    return rows


def d8_matrix(tiles):
    m = []
    for i in range(len(tiles)):
        for t in tiles[i]:
            m += tile_rows(t, i)
    return m


def print_tiles(row_list, counter):
    print('Solution %d:' % counter.value())
    print(row_list)


def d8_solve():
    matrix = d8_matrix(ends)
    head = make_objects(matrix, range(len(matrix[0])))
    counter = tile_solver.tile.SolutionCounter()
    search(head, callback=lambda r: print_tiles(r, counter))


# small board
corner_tiles = (corners,) * 4
# corner_tiles = ((corners[0],), (corners[1],), (corners[2],), (corners[3],))

end_tiles = (ends,) * 4
shorten_indices = [(0, 0), (1, 1), (2, 15), (3, 14), (4, 17), (5, 16), (6, 6),
                   (7, 7), (8, 8), (9, 9), (12, 25),
                   (13, 24), (18, 31), (19, 30),
                   (22, 22), (23, 23)]

border4 = (1,
           0, 0, 0, 0,
           1, 0, 0, 0,
           0, 0, 1, 0,
           1, 0,
           0, 0, 0, 0,
           1, 0)


def d4_matrix(tiles):
    m = [border4]
    for i in range(len(tiles)):
        for t in tiles[i]:
            m += tile_rows(t, i)
    return m


def shorten(row):
    return [row[s[0]] | row[s[1]] for s in shorten_indices]


# The matrix has NUM_TILES columns indicating the piece and
# 8 * WIDTH * HEIGHT columns indicating legal placements.
def tile_rows(tile, tile_number, num_tiles=4, width=2, height=2):
    """Return the rows for a given tile in a given orientation.

    Args:
        tile: 8-tuple representing the tile.
        tile_number: the tile index for this tile.

    Returns:
        List of rows to the matrix contributed by this tile (in this
        orientation).
    """
    prefix = [0] * (num_tiles + 1)
    prefix[tile_number + 1] = 1
    rows = []
    for pos in range(width * height):
        # Eliminate tiles that would protrude towards the top or left edge.
        if pos / width == 0 and tile[0] == 1:  # top is black
            continue
        if pos % width == 0 and tile[6] == 1:  # left is black
            continue
        row = prefix + shorten((pos * 8 * [0]) + list(tile) +
                               (width * height - pos - 1) * 8 * [0])
        rows.append(tuple(row))
    return rows


def d4_solve():
    matrix = d4_matrix(end_tiles)
    head = make_objects(matrix, range(len(matrix[0])))
    counter = tile_solver.tile.SolutionCounter()
    search(head, callback=lambda r: print_tiles(r, counter))


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    d = d4_matrix(corner_tiles)
    # for c in range(len(d[0])):
    #     print c - 5, sum([r[c] for r in d])
    d4_solve()
