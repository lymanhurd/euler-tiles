"""Implementation of Knuth's Dancing Links (DLX algorithm) for solving the
exact cover problem see:

http://arxiv.org/abs/cs/0011047

The particular application here is to use it in conjunction with a mapping
from the tiling problem,
"""
from __future__ import print_function

import logging

from node import Node, Column, Header


def make_objects(matrix, column_names):
    # Not checking for a square or non-empty matrix but that would be bad.
    num_rows = len(matrix)
    num_cols = len(matrix[0])
    assert len(column_names) == num_cols
    # Dict to keep track of nodes per column to fix left-right links when done.
    node_dict = {}
    # Header node is a special artificial placeholder in the list of columns.
    header = Header(num_cols)
    last_col = header
    cur_col = last_col
    for col_idx in range(num_cols):
        cur_col = Column(name=column_names[col_idx])
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
        cur_col.up = last_node
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
    return min(header.right_iter(), key=lambda x: x.size)


def cover_column(col):
    """
    Remove (cover) a column from the grid.

    Args:
        col: column object to remove.
    """
    logging.debug('Covering column %s size %d', col.name, col.size)
    col.h_remove()
    # Loop over all 1 nodes in the column.
    for col_node in col.down_iter():
        for row_node in col_node.right_iter():
            # Remove all 1 nodes from other columns in this row.
            row_node.v_remove()


def uncover_column(col):
    """
    Add (uncover) a column into the grid.

    Args:
        col: column object to add.
    """
    # For each row in the column.
    logging.debug('Uncovering column %s', col.name)
    for node in col.up_iter():
        # For each column with a 1 in this row.
        for row_node in node.left_iter():
            # Reinsert the node.
            row_node.v_restore()
    # Reinsert the column.
    col.h_restore()


def print_rows(rows):
    """
    A simple default program for displaying solutions, used for debugging.

    Args:
        rows: Solution expressed as a list of rows.
    """
    f1 = open('soln_file', 'a')
    print('Solution:', file=f1)
    for row in rows:
        solution = [row.column.name]
        for o in row.right_iter():
            solution.append(o.column.name)
        logging.info(solution)
        print(' '.join(solution), file=f1)


def search(header, rows=None, callback=print_rows, level=0):
    """
    Recursively solve the exact cover problem, which is given a matrix of 0's
    and 1's, find a subset of the rows such that every column has one and only
    one 1, or report that no such solution exists.  The arguments consist of
    the original matrix and the set of rows found so far.  When A becomes
    empty, we report the result to the callback (where we can print/save).

    In keeping with Knuth's paper, the matrices are represented as a doubly
    linked list of rows each of which is a double (and circularly) linked list
    of nodes corresponding to the 1's.

    Args:
        header: Original matrix, a linked list of rows objects.
        rows: Solution so far expressed as a list of rows.
        callback: function to which we report a solution.
        level: depth of search.
    """
    if rows is None:
        rows = []
    logging.debug('Searching level %d len rows = %d', level, len(rows))
    if header.right == header:
        callback(rows)
        return
    # Find a column with a minimal number of 1's to minimize branching.
    min_col = min_column(header)
    logging.debug('Min col = %s Size = %d', min_col.name, min_col.size)
    # Remove this column.
    cover_column(min_col)
    for row in min_col.down_iter():
        if level < len(rows):
            rows[level] = row
        else:
            rows.append(row)
        # By following the links we are finding every column which has a 1 in
        # this row.
        for col in row.right_iter():
            cover_column(col.column)
        search(header, rows, callback, level + 1)
        # Restore the columns which were removed.
        row = rows[level]
        for col in row.left_iter():
            uncover_column(col.column)
    # In the recursive case (level > 0) put the column back.
    uncover_column(min_col)
