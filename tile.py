"""Utilities for manipulating Euler tiles."""

import logging

import symmetries

__author__ = 'Lyman Hurd'


# Return the number of blank spaces in the given board and a board of the same dimensions assigning each blank a number
# with -1 indicating non-blank.
def enumerate_board(board):
    """Input a list of strings of the same length representing the board and returns a tuple consisting of the count of
    blanks and the enumerated board.

    Args:
        board: Board described as a list of strings.
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
    # matrix will have as many columns as num_tiles + empty space on board
    num_tiles = len(tiles)
    num_board, enumerated = enumerate_board(board)
    matrix = []
    # reduce symmetries by truncating one tile with maximal symmetry to a single one.
    for tile_num in range(num_tiles):
        sym_list = symmetries.symmetries(tiles[tile_num])
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


def naive_solve(solution, rows):
    logging.info(len(solution))
    if not rows:
        print solution
    else:
        for i in range(len(rows)):
            for s in solution:
                if max([sum(z) for z in zip(rows[i], s)]) >= 2:
                    return
            naive_solve(solution + [rows[i]], rows[:i] + rows[i + 1:])


def print_solution(row_list):
    pass

if __name__ == '__main__':
    pass
    # logging.basicConfig(level=logging.INFO)
    # m = cover_matrix(checkerboard, pents)
    # naive_solve([], m)
    # # solutions = solve(m)
    # # if not solutions:
    # #    print 'No solutions.'
    # # else:
    # #   for solution in solutions:
    # #       print_board(solution)
    # # print_solution(m)
    # print m
    # # print_solution(row_list)
