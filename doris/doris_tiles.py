__author__ = 'lhurd'

import logging

from dancing_links.links import make_objects, search

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

NUM_TILES = 24

NUM_EDGES = 36

NUM_COLORS = 3

BOARD = ((-1, -1, 0, 4), (0, -1, 1, 5), (1, -1, 2, 6),
         (2, -1, 3, 7), (3, -1, -1, 8), (-1, 4, 9, 13),
         (9, 5, 10, 14), (10, 6, 11, -1), (11, 7, 12, 15),
         (12, 8, -1, 16), (-1, 13, 17, 19), (17, 14, -1, 20),
         (-1, 15, 18, 21), (18, 16, -1, 22), (-1, 19, 23, 27),
         (23, 20, 24, 28), (24, -1, 25, 29), (25, 21, 26, 30),
         (26, 22, -1, 31), (-1, 27, 32, -1), (32, 28, 33, -1),
         (33, 29, 34, -1), (34, 30, 35, -1), (35, 31, -1, -1))

PATTERNS = ((1, 0, 0), (0, 1, 0), (0, 0, 1), (0, 1, 1), (1, 0, 1), (1, 1, 0))


def rotate(t, n):
    return t[n:] + t[:n]


def rotations(t):
    return set([rotate(t, n) for n in range(4)])


def tiles():
    tile_set = set()
    for i in range(81):
        t = (i % 3, (i / 3) % 3, (i / 9) % 3, (i / 27) % 3)
        t = min([rotate(t, n) for n in (0, 1, 2, 3)])
        tile_set.add(t)
    return sorted(tuple(tile_set))


def doris_matrix():
    matrix = []
    d_tiles = tiles()
    for i in range(NUM_TILES):
        for pos in BOARD:
            for t in rotations(d_tiles[3]):
                row = (NUM_TILES + NUM_EDGES * NUM_COLORS) * [0]
                row[i] = 1
                # TODO - fix this!
                if pos[0] != -1:
                    row[NUM_TILES + NUM_COLORS * pos[0]:
                    NUM_TILES + NUM_COLORS * pos[0] + 3] = PATTERNS[3 + t[0]]
                if pos[1] != -1:
                    row[NUM_TILES + NUM_COLORS * pos[1]:
                    NUM_TILES + NUM_COLORS * pos[1] + 3] = PATTERNS[3 + t[1]]
                if pos[2] != -1:
                    row[NUM_TILES + NUM_COLORS * pos[2]:
                    NUM_TILES + NUM_COLORS * pos[2] + 3] = PATTERNS[t[2]]
                if pos[3] != -1:
                    row[NUM_TILES + NUM_COLORS * pos[3]:
                    NUM_TILES + NUM_COLORS * pos[3] + 3] = PATTERNS[t[3]]
                matrix.append(row)
    return matrix


def print_solution(rows):
    logging.info('Found solution.')


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    dm = doris_matrix()
    head = make_objects(dm, range(len(dm[0])))
    search(head, callback=print_solution)
    print('Done')
