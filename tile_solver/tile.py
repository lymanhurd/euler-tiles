"""Utilities for manipulating tiles."""

import logging

import symmetries
from dancing_links.links import make_objects, search

__author__ = 'Lyman Hurd'


class SolutionCounter():
    def __init__(self):
        self.count = 0

    def value(self):
        self.count += 1
        return self.count


# Return the number of blank spaces in the given board and a board of the same dimensions assigning each blank a number
# with -1 indicating non-blank.
def enumerate_board(board):
    """Input a list of strings of the same length representing the board and returns a tuple consisting of the count of
    blanks and the enumerated board.

    Args:
        board: Board described as a list of strings where blanks indicate legal places to place a tile.
    """
    enumerated = [([-1] * len(board[0])) for i in range(len(board))]
    counter = 0
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == ' ':
                enumerated[r][c] = counter
                counter += 1
    return counter, enumerated


def covered_indices(board, tile, r, c):
    """Given an offset, an enumerated board and a tile, return a list of the locations that the tile would displace.  If
    the tile would overlap a location with a -1, indicating an illegal position, an empty string is returned.

    This method assumes that bounds checking has already been done (i.e., the tile will not leave the bounds of the
    board).

     Args:
         board: Enumerated board described as a list of numbers where non-negaive numbers indicate legal places to
         place.
           a tile.
         tile: tile to place.
         r; row offset.
         c: column offset.
     """
    indices = []
    for y in range(len(tile)):
        for x in range(len(tile[0])):
            if tile[y][x] != ' ':
                if board[y + r][x + c] == -1:
                    return []
                else:
                    indices.append(board[y + r][x + c])
    return indices


def cover_matrix(board, tiles):
    """Given a board, represent its tiling problem as an exact cover problem by representing a board with N spaces and
     a set of M tiles by a sequence of rows with N + M columns.  The first N columns will have exactly one 1, indicating
     which of the tiles is being represented, and then the 1's in the following columns will show the coordinates for
     a single legal placement of this tile (possibly including symmetries).

     Args:
         board: A board represented as a tuple of strings of equal length.
         tiles: an array of tiles (each one represented as a tuple of strings of equal length).
     """
    # matrix will have as many columns as num_tiles + empty space on board
    num_tiles = len(tiles)
    num_board, enumerated = enumerate_board(board)
    matrix = []
    # reduce symmetries by truncating one tile with maximal symmetry to a single one.
    for tile_num in range(num_tiles):
        if tile_num > 0:
            sym_list = symmetries.dihedral(tiles[tile_num])
        else:
            sym_list = [tiles[0]]
        # sym_list = symmetries.dihedral(tiles[tile_num])
        for t in sym_list:
            for r in range(len(board) - len(t) + 1):
                for c in range(len(board[0]) - len(t[0]) + 1):
                    # Will return indices of covered locations if the piece fits and [] otherwise.
                    indices = covered_indices(enumerated, t, r, c)
                    if indices:
                        row = (num_tiles + num_board) * [0]
                        row[tile_num] = 1
                        for idx in indices:
                            row[num_tiles + idx] = 1
                        matrix.append(row)
    return matrix


def print_tiles(board, row_list, counter):
    print 'Solution %d:' % counter.value()
    enumerated = enumerate_board(board)[1]
    d = {}
    for row in row_list:
        solution = [row.column.name]
        o = row.right
        while o != row:
            solution.append(o.column.name)
            o = o.right
        s = sorted(solution, reverse=True)
        for i in s[1:]:
            d[int(i)] = s[0]
    string_list = [''.join([d.get(t, ' ') for t in tile_row]) for tile_row in enumerated]
    print '\n'.join(string_list) + '\n'


def tile_solve(tile_set, board):
    # The errors produced if the tiles or the board are not rectangles will be hard to diagnose if the calculation is
    # allowed to proceed.
    assert isRectangle(board)
    for t in tile_set:
        assert isRectangle(t)
    column_names = [p[0].lstrip()[0] for p in tile_set]
    matrix = cover_matrix(board, tile_set)
    logging.debug(matrix)
    for i in range(len(matrix[0]) - len(column_names)):
        column_names.append(str(i))
    logging.debug(column_names)
    head = make_objects(matrix, column_names)
    counter = SolutionCounter()
    search(head, callback=lambda r: print_tiles(board, r, counter))


def isRectangle(m):
    s = [len(t) for t in m]
    return min(s) == max(s)
