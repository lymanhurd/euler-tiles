import logging

from links import make_objects, search

"""
The sample data structure in Knuth's paper reproduced for testing.
"""

example_row_names = ('C245', 'C036', 'C125', 'C03', 'C16', 'C346')

example_matrix = (
    (0, 0, 1, 0, 1, 1, 0),
    (1, 0, 0, 1, 0, 0, 1),
    (0, 1, 1, 0, 0, 1, 0),
    (1, 0, 0, 1, 0, 0, 0),
    (0, 1, 0, 0, 0, 0, 1),
    (0, 0, 0, 1, 1, 0, 1),
)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    head = make_objects(example_matrix, example_row_names)
    search(head)
