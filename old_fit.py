from euler_tiles.euler_boards import *
from euler_tiles.euler_tiles import *
from tile_solver.symmetries import *


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
    return ''.join(max(*t) for t in zip(x, y))


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


# Print a board.  Called when a solution has been found.
def print_board(b):
    logging.info('Solution found.')
    with open('solutions.txt', 'a') as f:
        print >> f, '+' + '-' * len(b[0]) + '+'
        for line in b:
            print >> f, '|' + line + '|'
        print >> f, '+' + '-' * len(b[0]) + '+'


def tile_8x8():
    board = ['***** ***', '        *', '         '] + ['        *'] * 6
    # board = [' ' * 8] * 8
    sym_list = [dihedral(t) for t in big_list]
    # force first element to have only one (out of 8) symmetries.
    sym_list[0] = [t7]
    fit_tiles(board, sym_list)


def tile_diamond():
    sym_list = [dihedral(t) for t in big_list]
    # force first element to have only one (out of 8) symmetries.
    sym_list[0] = [t7]
    fit_tiles(diamond, sym_list)


def tile_4x4():
    board = [' ' * 4] * 4
    sym_list = [dihedral(t) for t in small_list]
    fit_tiles(board, sym_list)


def tile_5x5():
    board = [' ' * 5] * 5
    sym_list = [dihedral(t) for t in big_list[:6]]
    sym_list[0] = [t7]
    fit_tiles(board, sym_list)


def tile_16x4():
    board = tuple([' ' * 16] * 4)
    sym_list = [dihedral(t) for t in big_list]
    # force first element to have only one (out of 8) symmetries.
    sym_list[0] = [t7]
    fit_tiles(board, sym_list)


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
