# 8x8
chess_board = tuple(8 * ['        '])

# This is a known solvable position for testing purposes,  It represnts an "almost" solution to the 8x8.
jay_board = (
    '***** ***',
    '        *',
    '         ',
    '        *',
    '    *   *',
    '        *',
    '    *   *',
    '        *',
    '        *',
)

lyman_board = (
    '******** ',
    '         ',
    '        *',
    '        *',
    '        *',
    '        *',
    '        *',
    '        *',
    '**      *',
)

# Pattern 2:
diamond = (
    '*****  *****',
    '*****  *****',
    '****    ****',
    '****    ****',
    '**        **',
    '            ',
    '            ',
    '**        **',
    '****    ****',
    '****    ****',
    '*****  *****',
    '*****  *****',
)

# Checkboard minus 4.
checkerboard = (
    '        ',
    '        ',
    '        ',
    '   **   ',
    '   **   ',
    '        ',
    '        ',
    '        ',
)

castle = (
    '   xxx   ',
    '         ',
    '         ',
    'X  XXX  X',
    'X  XXX  X',
    'X  XXX  X',
    'X  XXX  X',
    '         ',
    '         ',
    '   xxx   ',
)

plus = (
    'xxx    xxx',
    'xxx    xxx',
    'xxx    xxx',
    '          ',
    '          ',
    '          ',
    '          ',
    'xxx    xxx',
    'xxx    xxx',
    'xxx    xxx',
)
