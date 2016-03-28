"""Implementation of Knuth's Dancing Links (DLX algorithm) for solving the exact cover problem see:

http://arxiv.org/abs/cs/0011047

The particular application here is to use it in conjuction with a mapping frmo the tling problem,
"""

from node import Node, Column


def make_objects(matrix, column_names):
    # Not checking for a square or non-empty matrix but that would be bad.
    num_rows = len(matrix)
    num_cols = len(matrix[0])
    assert len(column_names) == num_cols
    # Dict to keep track of nodes per column to fix left-right links when done.
    node_dict = {}
    # Header node is a special artificial placeholder in the list of columns.
    header = Node()
    header.size = num_cols  # Different from the paper but a convenient place to hold this value.
    last_col = header
    cur_col = last_col
    for col_idx in range(num_cols):
        cur_col = Column(name=column_names[col_idx], size=0)
        # Populate the nodes in this column.
        last_node = cur_col
        cur_node = cur_col
        for row_idx in range(num_rows):
            if matrix[row_idx][col_idx]:
                cur_node = Node(column=cur_col, up=last_node)
                node_dict[(row_idx, col_idx)] = cur_node
                last_node.down = cur_node
                last_node = cur_node
                cur_col.size += 1
        cur_node.down = cur_col
        last_col.right = cur_col
        cur_col.left = last_col
        last_col = cur_col
    # The very last column loops back to the header.
    cur_col.right = header
    header.left = cur_col
    # Fix left-right links among nodes in each column.
    for row_idx in range(num_rows):
        initial_node = None
        last_node = None
        cur_node = initial_node
        for col_idx in range(num_cols):
            if (row_idx, col_idx) in node_dict:
                cur_node = node_dict[(row_idx, col_idx)]
                if not initial_node:
                    initial_node = cur_node
                cur_node.left = last_node
                if last_node:
                    last_node.right = cur_node
                last_node = cur_node
        last_node.right = initial_node
        initial_node.left = cur_node
    return header


def min_column(header):
    """Find column with the fewest number of 1's.

    Args:
        header: pointer to a data structure representing the array.

    Returns:
        column object with the fewest 1's.
    """
    min_size = 99999
    col = header.right
    min_col = col
    while col != header:
        if col.size < min_size:
            min_size = col.size
            min_col = col
        col = col.right
    return min_col


def cover_column(col):
    """
    Remove (cover) a column from the grid.

    Args:
        col: column object to remove.
    """
    col.right.left = col.left
    col.left.right = col.right
    # Loop over all 1 nodes in the column.
    node = col.down
    while node != col:
        row_node = node.right
        # Remove all 1 nodes from other columns in this row.
        while row_node != node:
            row_node.down.up = row_node.up
            row_node.up.down = row_node.down
            row_node = row_node.right
            row_node.column.size -= 1
        node = node.down
    col.size -= 1


def uncover_column(col):
    """
    Add (uncover) a column into the grid.

    Args:
        col: column object to add.
    """
    # For each row in the column.
    node = col.up
    while node != col:
        # For each column with a 1 in this row.
        row_node = node.left
        while row_node != node:
            # Reinsert the node.
            row_node.down.up = row_node
            row_node.up.down = row_node
            row_node = row_node.left
            row_node.column.size += 1
        node = node.up
    # Reinsert the column.
    col.right.left = col
    col.left.right = col
    col.size += 1


def print_rows(rows, level):
    solution = []
    for row in rows[:level]:
        solution.append(row.column.name)
    print ' '.join(solution)


def search(head, rows=None, callback=print_rows, level=0):
    """
    Recursively solve the exact cover problem, which is given a matrix of 0's and 1's, find a subset of the rows such
    that every column has one and only one 1, or report that no such solution exists.  The arguments consist of the
    original matrix and the set of rows found so far.  When A becomes empty, we report the result to the callback (where
    we can print/save).

    In keeping with Knuth's paper, the matrices are represented as a doubly linked list of rows each of which is a
    double (and circularly) linked list of nodes corresponding to the 1's.

    Args:
        head: Original matrix, a linked list of rows objects.
        rows: Solution so far expressed as a list of rows.
        callback: function to which we report a solution.
        level: depth of search.

    """
    if level == 0:
        rows = [None] * head.size
    if head.right == head:
        callback(rows, level)
        return
    min_col = min_column(head)
    cover_column(min_col)
    row = min_col.down
    while row != min_col:
        rows[level] = row
        col = row.right
        while col != row:
            cover_column(col.column)
            col = col.right
        search(head, rows, callback, level + 1)
        row = rows[level]
        col = row.left
        while col != row:
            uncover_column(col.column)
            col = col.left
    uncover_column(min_col)