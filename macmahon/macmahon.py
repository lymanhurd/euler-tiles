__author__ = 'lhurd'

import logging

from dancing.links import make_objects, search

WIDTH = 6
HEIGHT = 4

# the set of tiles is identical to those in the Doris puzzle, however the interpretation differs
TILES = (
    (0, 0, 0, 0),  # [0] (red, red, red, red)
    (0, 0, 0, 1),  # [1] (red, red, red, green)
    (0, 0, 0, 2),  # [2] (red, red, red, orange)
    (0, 0, 1, 1),  # [3] (red, red, green, green)
    (0, 0, 1, 2),  # [4] (red, red, green, orange)
    (0, 0, 2, 1),  # [5] (red, red, orange, green)
    (0, 0, 2, 2),  # [6] (red, red, orange, orange)
    (0, 1, 0, 1),  # [7] (red, green, red, green)
    (0, 1, 0, 2),  # [8] (red, green, red, orange)
    (0, 1, 1, 1),  # [9] (red, green, green, green)
    (0, 1, 1, 2),  # [10] (red, green, green, orange)
    (0, 1, 2, 1),  # [11] (red, green, orange, green)
    (0, 1, 2, 2),  # [12] (red, green, orange, orange)
    (0, 2, 0, 2),  # [13] (red, orange, red, orange)
    (0, 2, 1, 1),  # [14] (red, orange, green, green)
    (0, 2, 1, 2),  # [15] (red, orange, green, orange)
    (0, 2, 2, 1),  # [16] (red, orange, orange, green)
    (0, 2, 2, 2),  # [17] (red, orange, orange, orange)
    (1, 1, 1, 1),  # [18] (green, green, green, green)
    (1, 1, 1, 2),  # [19] (green, green, green, orange)
    (1, 1, 2, 2),  # [20] (green, green, orange, orange)
    (1, 2, 1, 2),  # [21] (green, orange, green, orange)
    (1, 2, 2, 2),  # [22] (green, orange, orange, orange)
    (2, 2, 2, 2))  # [23] (orange, orange, orange, orange)


COLOR_TUPLES1 = ((0, 0), (1, 0), (0, 1))


COLOR_TUPLES2 = ((1, 1), (0, 1), (1, 0))

COLOR_NAMES = ("R", "G", "O")

def color_name(tile):
    return f"({COLOR_NAMES[tile[0]]},{COLOR_NAMES[tile[1]]},{COLOR_NAMES[tile[2]]},{COLOR_NAMES[tile[3]]})"

# due to symmetry, every tile has 1, 2 or 4 distinct orientations
# the total number of distinct oriented tiles in 81


NUM_TILES = len(TILES)


# the matrix associated with a tiling has one row for every tile indicating which tile is in which position in which
# orientation.  The first NUM_TILES column will have a 1 in the position corresponding to the number of that tile to
# ensure that the final solution uses every tile exactly once.  The remaining columns ensure that the edge matching
# conditions are met.  For an array that is WIDTH x HEIGHT (here WIDTH = 6 and HEIGHT = 6), there are:
# (WIDTH - 1) * HEIGHT + WIDTH * (HEIGHT - 1) places where tiles meet.
# in our example this leads to 48 edges.

# These internal edge constraints are in addition to the constraint that the outer border must have a single color
# which, without loss of generality, we assume is red.

# the edge color is represented by two bits. The North and East edges the colors are represented as:
# RED: (0, 0) GREEN: (0, 1), ORANGE: (1, 0)
# The south and west edged by:
# RED: (1, 1) GREEN: (1, 0), ORANGE: (0, 1)

# fixing the outer color eliminates 2/3 of possible solutions.  Also given that the outer color is fixed as red,
# any solution can be transformed by swapping green for orange.

# this symmetry can be factored in by making sure that the (green, orange, green, orange) tile, (1, 2, 1, 2) can
# only occur in one orientation since rotating it by 90 degrees would be equivalent to swapping green and orange.

# the last symmetries are based on the dihedral symmetries of the rectangle, i.e., reflection vertically or horizontally
# the dihedral symmetries can be factored in by making sure that the all red tile occupies a position in the upper left
# quadrant


def check_boundary(i, j, t):
    """
    Checks whether a tile agrees with the boundary condition that all external edges are red.

    Args:
        i: row
        j: col
        t: oriented tile (tuple)

    Returns:
        true if the boundary of the tile matches the edge condition (i.e., red)
    """
    if i == 0 and t[0] != 0:
        return False
    if i == HEIGHT - 1 and t[2] != 0:
        return False
    if j == 0 and t[3] != 0:
        return False
    if j == WIDTH - 1 and t[1] != 0:
        return False
    return True


def check_orientation(i, j, t):
    """
    Returns false if the tile is all red (0, 0, 0, 0) and not in the upper right quadrant.

    Args:
        i: row
        j: column
        t: oriented tile

    Returns:

    """
    return t != (0, 0, 0, 0) or (i < HEIGHT // 2 and j < WIDTH // 2)



def macmahon_matrix():
    """
    Constructs the open cover matrix corresponding to the tiling problem.

    Returns:
        0-1 matrix defined in such a way that a valid tiling consists of choosing a subset of the rows so that every
        column has exactly one 1.
    """
    matrix = []
    rn = []
    for i in range(HEIGHT):
        for j in range(WIDTH):
            for n, tile in enumerate(TILES):
                if not check_orientation(i, j, tile):
                    continue
                for t in rotations(tile):
                    # eliminate any tiles that do not match the outer boundary
                    if not check_boundary(i, j, t):
                        continue
                    # eliminate one of the rotations of the (1, 2, 1, 2) tile
                    if t == (2, 1, 2, 1):
                        continue
                    idx = i * WIDTH + j
                    row = [0] * idx + [1] + [0] * (WIDTH * HEIGHT - idx - 1)
                    #  the next NUM_TILES columns indicate which tile is used
                    row += [0] * n + [1] + [0] * (NUM_TILES - n - 1)
                    rn.append(f"({i}, {j}) -> {color_name(t)}")
                    row += edge_constraints(i, j, t)
                    matrix.append(row)
    return matrix, rn


def edge_constraints(i, j, t):
    vertical = [0] * 2 * ((WIDTH - 1) * HEIGHT)
    # Set right constraints
    if j < WIDTH - 1:
        vertical[2 * (j + i * (WIDTH - 1))], vertical[2 * (j + i * (WIDTH - 1)) + 1] = COLOR_TUPLES1[t[1]]
    # Set left constraints
    if j > 0:
        vertical[2 * (j - 1 + i * (WIDTH - 1))], vertical[2 * (j - 1 + i * (WIDTH - 1)) + 1] = COLOR_TUPLES2[t[3]]

    horizontal = [0] * (2 * WIDTH * (HEIGHT - 1))
    # Set bottom constraints
    if i < HEIGHT - 1:
        horizontal[2 * (j + i * WIDTH)], horizontal[2 * (j + i * WIDTH) + 1] = COLOR_TUPLES1[t[2]]
    # Set top constraints
    if i > 0:
        horizontal[2 * (j + (i - 1) * WIDTH)], horizontal[2 * (j + (i - 1) * WIDTH) + 1] = COLOR_TUPLES2[t[0]]
    return vertical + horizontal


def rotations(t):
    return {tuple(t[n:] + t[:n]) for n in range(4)}

def make_solution_function():
    def generator():
        n = 1
        while True:
            yield f"Solution {n}"
            n += 1

    gen = generator()

    def next_solution(ignored):
        print(next(gen))

    return next_solution

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    dm, row_names = macmahon_matrix()
    # for i, r in enumerate(row_names):
    #     print(f"{r} {dm[i]}")
    callback = make_solution_function()
    head = make_objects(dm, row_names)
    search(head, callback=callback)
