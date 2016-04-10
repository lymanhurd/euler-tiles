import logging

from boards import jay_board
from tile import tile_solve

t1 = ('a',)

t2 = ('bb',)

t3 = ('cc', ' c')

t4 = ('dd ', ' dd')

t5 = ('eee', ' e ')

t6 = (' f ', 'fff', ' f ')

t7 = (' gg', 'gg ', ' g ')

t8 = ('h  ', 'hh ', ' hh')

t9 = (' i ', 'iii', ' i ', ' i ')

t10 = (' j ', ' jj', 'jj ', ' j ')

t11 = ('k k', 'kkk', ' k ')

t12 = ('ll ', 'lll', ' l ')

t13 = ( '  m', ' mm', 'mm ', 'm  ')

t14 = ('  n', ' nn', 'nn ', ' n ')

big_list = [t7, t2, t3, t4, t5, t6, t8, t9, t10, t11, t12, t13, t14]

small_list = [t2, t3, t4, t5]

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    tile_solve(big_list, jay_board)
