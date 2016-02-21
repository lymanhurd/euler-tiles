"""Utilities for manipulating Euler tiles."""

from euler_tiles import *
import logging

__author__ = 'Lyman Hurd'


# A legal tile must have no blank rows and no blank columns.

def tile_height(tile):
    return len(tile)


def tile_width(tile):
    return len(tile[0])


def vflip(tile):
    return tile[::-1]


def hflip(tile):
    return tuple(t[::-1] for t in tile)


def dflip(tile):
    return tuple(''.join(t) for t in zip(*tile))


def can_fit(board, tile, i, j):
    if len(board) < len(tile) + j:
        return False
    if len(board[0]) < len(tile[0]) + i:
        return False
    for y in range(len(tile)):
        if max([len(''.join(t).strip()) for t in zip(tile[y], board[y+j][i:])]) > 1:
            return False
    return True


def merge(board, tile, i, j):
    return tuple(list(board[:j]) +
                 [merge_lines(board[j + y], ' ' * i + tile[y] + ' ' * (len(board[0]) - len(tile[0]) - i))
                  for y in range(len(tile))] + list(board[j + len(tile):]))


def merge_lines(x, y):
    logging.debug('%d, %d', len(x), len(y))
    return ''.join(max(*t) for t in zip(x,y))


def symmetries(tile):
    symmetries = [tile]
    symmetries += [dflip(t) for t in symmetries]
    symmetries += [hflip(t) for t in symmetries]
    symmetries += [vflip(t) for t in symmetries]
    return list(set(symmetries))


def fit_tiles(board, tiles):
    logging.debug('Called with %s and %s', board, len(tiles))
    boards = []
    for tile in tiles[0]:
        for j in range(len(board)):
            for i in range(len(board[0])):
                if can_fit(board, tile, i, j):
                    boards.append(merge(board, tile, i, j))
    if len(tiles) > 1:
        result = []
        for b in boards:
            result.extend(fit_tiles(b,tiles[1:]))
    else:
        result = boards
        for b in boards:
            print_board(b)
    return result


def print_board(b):
    with open('solutions.txt', 'a') as f:
        print >>f, '+' + '-' * len(b[0]) + '+'
        for line in b:
            print >>f,  '|' + line + '|'
        print >>f, '+' + '-' * len(b[0]) + '+'


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    # board = ('yyyyyyy', 'y     y', 'y     y', 'y     y', 'yyyyyyy')
    # tile = (' xx', 'xx ', ' x ')
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
    board = tuple([' ' * 8] * 8)
    sym_list = [symmetries(t) for t in big_list]
    # force first element to have only one (out of 8) symmetries.
    sym_list[0] = [t7]
    bds = fit_tiles(board, sym_list)
    if len(bds) > 0:
        print 'Found %d solutions.' % len(bds)
    else:
        print 'Found no solutions.'
    # for b in bds:
    #     print_board(b)
    #     print '\n'
    # for t in big_list:
    #     for s in symmetries(t):
    #         print_board(s)