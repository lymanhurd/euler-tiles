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

# The pentominoes here for benchmarking since the solution counts are well established.

pentF = (' ff', 'ff ', ' f ')

pentI = ('iiiii')

pentL = ('l  ', 'l  ', 'lll')

pentP = ('pp', 'pp', 'p ')

pentN = ('n ', 'n ', 'nn', ' n')

pentT = ('ttt', ' t ', ' t ')

pentU = ('u u', 'uuu')

pentV = ('v  ', 'v  ', 'vvv')

pentW = ('w  ', 'ww ', ' ww')

pentX = (' x ', 'xxx', ' x ')

pentY = ('  y ', 'yyyy')

pentZ = ('  z', 'zzz', 'z  ')

pentominoes = (pentF, pentI, pentL, pentP, pentN, pentT, pentU, pentV, pentW, pentX, pentY, pentZ)
