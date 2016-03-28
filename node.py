"""
This class represents the 1's in the matrix.  The Nodes are formed into circularly linked lists to make rows (i.e.,
joined by Left/Right and vertically linked lists to make columns.  In addition, each node contains a link to the column
which contains it.  For the purposes of the algorithm, rows all are treated symetrically and therefore do not need to
be tracked.
"""


class Node:
    def __init__(self, left=None, right=None, up=None, down=None, column=None):
        self.left = left
        self.right = right
        self.up = up
        self.down = down
        self.column = column

    def __repr__(self):
        if self.column:
            return 'Node(%s)' % self.column.name
        else:
            return 'Header'


class Column(Node):
    def __init__(self, left=None, right=None, up=None, down=None, size=0, name=None):
        Node.__init__(self, left=left, right=right, up=up, down=down)
        self.size = size
        self.name = name
        self.column = self

    def __repr__(self):
        return 'Column(%s)' % self.name
