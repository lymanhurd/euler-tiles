import logging

from dancing_links import make_objects, search

"""
The sample data structure in Knuth's paper reproduced for testing.
"""

example_column_names = ('A', 'B', 'C', 'D', 'E', 'F', 'G')

example_matrix = (
    (0, 0, 1, 0, 1, 1, 0),
    (1, 0, 0, 1, 0, 0, 1),
    (0, 1, 1, 0, 0, 1, 0),
    (1, 0, 0, 1, 0, 0, 0),
    (0, 1, 0, 0, 0, 0, 1),
    (0, 0, 0, 1, 1, 0, 1),
)

if __name__ == '__main__':
    logging.basicConfig(level=logging.WARN)
    head = make_objects(example_matrix, example_column_names)
    search(head)
