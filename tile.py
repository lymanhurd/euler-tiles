"""Utilities for manipulating Euler tiles."""

import logging

from boards import *
from euler_tiles import *
from symmetries import *

__author__ = 'Lyman Hurd'


# Return the number of blank spaces in the given board and a board of the same dimensions assigning each blank a number
# with -1 indicating non-blank.
def enumerate_board(board):
    """Input a list of strings of the same length representing the board and returns a tuple consisting of the count of
    blanks and the enumerated board."""
    enumerated = [([-1] * len(board[0])) for i in range(len(board))]
    counter = 0
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == ' ':
                enumerated[r][c] = counter
                counter += 1
    return counter, enumerated


def covered_indices(board, tile, i, j):
    indices = []
    for y in range(len(tile)):
        for x in range(len(tile[0])):
            if tile[y][x] != ' ':
                if board[y + j][x + i] == -1:
                    return []
                else:
                    indices.append(board[y + j][x + i])
    return indices


def cover_matrix(board, tiles):
    # matrix will have as many columns as num_tiles + empty space on board
    num_tiles = len(tiles)
    num_board, enumerated = enumerate_board(board)
    matrix = []
    for tile_num in range(num_tiles):
        sym_list = symmetries(tiles[tile_num])
        for t in sym_list:
            for r in range(len(board) - len(t)):
                for c in range(len(board[0]) - len(t[0])):
                    # Will return indices of covered locations if the piece fits and [] otherwise.
                    indices = covered_indices(enumerated, t, r, c)
                    if indices:
                        row = (num_tiles + num_board) * [0]
                        row[tile_num] = 1
                        for idx in indices:
                            row[num_tiles + idx] = 1
                        matrix.append(row)
    return matrix


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    m = cover_matrix(diamond, big_list)
    # solutions = solve(m)
    # if not solutions:
    #    print 'No solutions.'
    # else:
    #   for solution in solutions:
    #       print_board(solution)
    # print_solution(m)
    print m
