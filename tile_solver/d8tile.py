__author__ = 'lhurd'


def rot2(tile):
    return tuple([tile[i:] + tile[:i] for i in (0, 2,)])


def rot4(tile):
    return tuple([tile[i:] + tile[:i] for i in (0, 2, 4, 6,)])


# The sides are enumerated clockwise.  (1, 0) means black, and (0, 1) white.
corner = (1, 0, 1, 0, 1, 0, 0, 1,)
end = (1, 0, 0, 1, 0, 1, 0, 1,)
straight = (1, 0, 0, 1, 1, 0, 0, 1)
tee = (1, 0, 1, 0, 1, 0, 0, 1)
cross = (1, 0, 1, 0, 1, 0, 1, 0)

corners = rot4(cross)
ends = rot4(end)
straights = rot2(straight)
tees = rot4(tee)
crosses = (cross,)


# There are 4 corners, 4 ends, 1 straight, 4 tees, 3 crosses in the tile set.
d8tiles = (corners,) * 4 + (ends,) * 4 + (straights,) + (tees,) * 4 + (
                                                                      crosses,) * 3

# The matrix has 16 columns indicating the piece and 64 columns indicating legal placements.


def tile_rows(tile, tile_number):
    """Return the rows for a given tile in a given orientation.

    Args:
        tile: 8-tuple representing the tile.
        tile_number: the tile 0-15 for this tile.

    Returns:
        list of rows to the matrix contributed by this tile (in this orientation).
    """
    prefix = [0] * 16
    prefix[tile_number] = 1
    rows = []
    for r in range(4):
        for c in range(4):
            # Eliminate tiles that would protrude towards the top or left edge.
            if r == 0 and tile[6]:
                continue
            if c == 0 and tile[4]:
                continue
            row = [0] * 64
            row[4 * (4 * r + c)] = tile[0]
            row[4 * (4 * r + c) + 1] = tile[1]
            row[4 * (4 * r + c) + 2] = tile[2]
            row[4 * (4 * r + c) + 3] = tile[3]
            if c > 0:
                row[4 * (4 * r + c - 1) + 0] = tile[5]
                row[4 * (4 * r + c - 1) + 1] = tile[4]
            if r > 0:
                row[4 * (4 * (r - 1) + c) + 2] = tile[7]
                row[4 * (4 * (r - 1) + c) + 3] = tile[6]
            rows.append(prefix + row)
    return rows


def d8matrix():
    m = []
    for i in range(16):
        for t in d8tiles[i]:
            m += tile_rows(t, i)
    return m


if __name__ == '__main__':
    matrix = d8matrix()
    print len(matrix)
    # for r in matrix:
    #     print r
