import logging

from boards import checkerboard
from tile import tile_solve

# The pentominoes here for benchmarking since the solution counts are well established.

pentF = (' ff', 'ff ', ' f ')

pentI = ('iiiii',)

pentL = ('l   ', 'llll')

pentP = ('pp', 'pp', 'p ')

pentN = ('n ', 'n ', 'nn', ' n')

pentT = ('ttt', ' t ', ' t ')

pentU = ('u u', 'uuu')

pentV = ('v  ', 'v  ', 'vvv')

pentW = ('w  ', 'ww ', ' ww')

pentX = (' x ', 'xxx', ' x ')

pentY = ('  y ', 'yyyy')

pentZ = ('  z', 'zzz', 'z  ')

pents = (pentF, pentI, pentL, pentP, pentN, pentT, pentU, pentV, pentW, pentX, pentY, pentZ)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    tile_solve(pents, checkerboard)
