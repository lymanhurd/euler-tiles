"""Utilities for manipulating Euler tiles."""

import logging

from euler_tiles import *

__author__ = 'Lyman Hurd'


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
    symmetries = [tile]
    symmetries += [dflip(t) for t in symmetries]
    symmetries += [hflip(t) for t in symmetries]
    symmetries += [vflip(t) for t in symmetries]
    return list(set(symmetries))


# Determine if a specific tile can fit onto the board at a specific position.  The call has no range checking,
# as this has been assumed to be done by the caller.

def can_fit(board, tile, i, j):
    for y in range(len(tile)):
        for x in range(len(tile[0])):
            if tile[y][x] != ' ' and board[y + j][x + i] != ' ':
                return False
    return True


# Return a new board with the given tile merged.
def merge(board, tile, i, j):
    prepad = ' ' * i
    postpad = ' ' * (len(board[0]) - len(tile[0]) - i)
    return (board[:j] +
            [merge_lines(board[j + y], prepad + tile[y] + postpad) for y in range(len(tile))] +
            board[j + len(tile):])


def merge_lines(x, y):
    return ''.join(max(*t) for t in zip(x,y))


def fit_tiles(board, tiles):
    if not tiles:
        print_board(board)
        return
    if len(tiles) > 7:
        logging.info('Called with %s tiles', len(tiles))
    for tile in tiles[0]:
        for j in range(len(board) - len(tile) + 1):
            for i in range(len(board[0]) - len(tile[0]) + 1):
                if can_fit(board, tile, i, j):
                    fit_tiles(merge(board, tile, i, j), tiles[1:])


# Print a board.  Called whena  solution has been found.

def print_board(b):
    logging.info('Solution found.')
    with open('solutions.txt', 'a') as f:
        print >>f, '+' + '-' * len(b[0]) + '+'
        for line in b:
            print >>f,  '|' + line + '|'
        print >>f, '+' + '-' * len(b[0]) + '+'


def tile_8x8():
    board = ['***** ***', '        *', '         '] + ['        *'] * 6
    # board = [' ' * 8] * 8
    sym_list = [symmetries(t) for t in big_list]
    # force first element to have only one (out of 8) symmetries.
    sym_list[0] = [t7]
    fit_tiles(board, sym_list)


def tile_4x4():
    board = [' ' * 4] * 4
    sym_list = [symmetries(t) for t in small_list]
    fit_tiles(board, sym_list)


def tile_5x5():
    board = [' ' * 5] * 5
    sym_list = [symmetries(t) for t in big_list[:6]]
    sym_list[0] = [t7]
    fit_tiles(board, sym_list)


def tile_16x4():
    board = tuple([' ' * 16] * 4)
    sym_list = [symmetries(t) for t in big_list]
    # force first element to have only one (out of 8) symmetries.
    sym_list[0] = [t7]
    fit_tiles(board, sym_list)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    tile_5x5()
    # board = ('yyyyyyy', 'y      ', 'y      ', 'y      ', 'yyyyyyy')
    # tile = ('xx', 'xx ', ' x ')
    # s = symmetries(tile)
    # for t in s:
    #     print t
    # for i in range(len(board[0])):
    #     for j in range(len(board)):
    #         fits = can_fit(board, tile, i, j)
    #         print '(%d, %d) = %s' % (i, j, fits)
    #         if fits:
    #             merged = merge(board, tile, i, j)
    #             for line in merged:
    #                 print line
