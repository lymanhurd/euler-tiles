import logging
from links import make_objects, search

RED = (1, 0, 0, 0)
GREEN = (0, 1, 0, 0)
BLUE = (0, 0, 1, 0)
YELLOW = (0, 0, 0, 1)
CUBES = ["RYGBRG", "RBYGBY", "RBYGGB", "RRYGBR"]
COLORS = {
    "R": [1, 0, 0, 0],
    "G": [0, 1, 0, 0],
    "B": [0, 0, 1, 0],
    "Y": [0, 0, 0, 1]
}
COLOR_TO_LETTERS = {
    (1, 0, 0, 0): "R",
    (0, 1, 0, 0): "G",
    (0, 0, 1, 0): "B",
    (0, 0, 0, 1): "Y"
}
# Reducing values in ORIENTATION_LIST by 1 so that they match String indices instead of matching actual
# die sides.
ORIENTATION_LIST = [[1, 2, 4, 3], [2, 4, 3, 1], [4, 3, 1, 2], [3, 1, 2, 4], [5, 2, 0, 3], [2, 0, 3, 5],
                    [0, 3, 5, 2], [3, 5, 2, 0], [5, 2, 0, 3], [2, 0, 3, 5], [0, 3, 5, 2], [3, 5, 2, 0],
                    [4, 2, 1, 3], [2, 1, 3, 4], [1, 3, 4, 2], [3, 4, 2, 1], [1, 0, 4, 5], [0, 4, 5, 1],
                    [4, 5, 1, 0], [5, 1, 0, 4], [1, 5, 4, 0], [5, 4, 0, 1], [4, 0, 1, 5], [0, 1, 5, 4]]


def initialize_matrix():
    # m = []
    # for cube in range(4):
    #    for o in range(24):
    #       m.append(generate_row(cube, o))
    # m = [generate_row(cube, o) for cube in range(4) for o in range(24)]
    result = []
    for i in range(4):
        for j in range(24):
            matrix_entry = generate_row(i, show_colors(j, i))
            result.append(matrix_entry)
    return result


# go from cube, orientation to string with four colors
def show_colors(orientation, cube):
    return "".join([CUBES[cube][i] for i in ORIENTATION_LIST[orientation]])
    # for i in ORIENTATION_LIST[orientation]:
    #     result += CUBES[cube][i]
    #     print(i, result)
    # return result


# take dice number and faces (from show_colors) and produce matrix row
def generate_row(cube, faces):
    row = [0, 0, 0, 0]
    row[cube] = 1
    for i in faces:
        row += COLORS[i]
    return row


# print the result of a row
def display_row(vector):
    # TODO also prepend piece number (e.g., 3 BYGR)
    result = ""
    for x in range(4, len(vector), 4):
        result += COLOR_TO_LETTERS[tuple(vector[x:x + 4])]
    print(result)


def check_for_3(matrix):
    for i in range(4):  # determines column
        result = []
        for j in range(4):  # determines row
            result += display_row(matrix[j][i])
        print(result)


# possible TODO make sure we sort the rows by the piece number...
def print_solution(rows):
    print("___________________________________")
    for r in rows:
        print(display_row(r))
    logging.info('Found solution.')


# if __name__ == '__main__':
#     # matrix = [[[1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1] for i in range(10)] for j in range(10)]
#     faces = show_colors(0, 0)
#     row = generate_row(3, faces)
#     display_row(row)
#     # check_for_3(matrix)
#     matrix = initialize_matrix()

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    iim = initialize_matrix()
    head = make_objects(iim, list(range(len(iim[0]))))
    search(head, callback=print_solution)
    print('Done')