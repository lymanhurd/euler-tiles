import logging

from boards import checkerboard
from dancing_links import make_objects, search
from tile import cover_matrix

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

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    column_names = [p[0].lstrip()[0] for p in pentominoes]
    matrix = cover_matrix(checkerboard, pentominoes)
    logging.debug(matrix)
    for i in range(len(matrix[0]) - len(column_names)):
        column_names.append(str(i))
    logging.debug(column_names)
    head = make_objects(matrix, column_names)
    search(head)
