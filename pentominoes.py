import logging

from boards import checkerboard
from dancing_links import make_objects, search
from tile import cover_matrix, print_tiles, SolutionCounter

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
    column_names = [p[0].lstrip()[0] for p in pents]
    matrix = cover_matrix(checkerboard, pents)
    logging.debug(matrix)
    for i in range(len(matrix[0]) - len(column_names)):
        column_names.append(str(i))
    logging.debug(column_names)
    head = make_objects(matrix, column_names)
    counter = SolutionCounter()
    search(head, callback=lambda r: print_tiles(checkerboard, r, counter))
