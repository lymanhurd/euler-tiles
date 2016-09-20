"""
This class represents the 1's in the matrix.  The Nodes are formed into circularly linked lists to make rows (i.e.,
joined by Left/Right and vertically linked lists to make columns.  In addition, each node contains a link to the column
which contains it.  For the purposes of the algorithm, rows all are treated symmetrically and therefore do not need to
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
            return 'Node'

    # The central "point" of Knuth's paper is the fact that if you do not destroy of alter an object removed from a
    # circularly linked list, you can put it back in constant time which greatly facilitates back-tracking.
    def v_remove(self):
        self.down.up = self.up
        self.up.down = self.down
        self.column.size -= 1

    def v_restore(self):
        self.down.up = self
        self.up.down = self
        self.column.size += 1

    # Horizontal traversla is only ever undertaken starting at column objects, but for symmetry the method is also
    # defined in the Node class.
    def h_remove(self):
        self.right.left = self.left
        self.left.right = self.right

    def h_restore(self):
        self.right.left = self
        self.left.right = self

    # Iterators for traversing circular linked lists back to the starting point.  In the form needed in the algorithm,
    # these iterators never return themselves but iterate over all other elements in the given direction.
    def right_iter(self):
        node = self.right
        while node != self:
            yield node
            node = node.right

    def left_iter(self):
        node = self.left
        while node != self:
            yield node
            node = node.left

    def up_iter(self):
        node = self.up
        while node != self:
            yield node
            node = node.up

    def down_iter(self):
        node = self.down
        while node != self:
            yield node
            node = node.down


class Column(Node):
    def __init__(self, left=None, right=None, up=None, down=None, size=0, name=None):
        Node.__init__(self, left=left, right=right, up=up, down=down)
        self.size = size
        self.name = name
        self.column = self

    def __repr__(self):
        return 'Column(%s)' % self.name


class Header(Column):
    def __init__(self, num_cols=0):
        Column.__init__(self, size=0, name='Header')
        self.num_cols = num_cols


# Static utilities...


def link_left_right(node_list):
    num_elements = len(node_list)
    for i in range(num_elements):
        node_list[i].right = node_list[i + 1 % num_elements]
        node_list[i + 1 % num_elements].left = node_list[i]


def link_up_down(node_list):
    num_elements = len(node_list)
    for i in range(num_elements):
        node_list[i].down = node_list[i + 1 % num_elements]
        node_list[i + 1 % num_elements].up = node_list[i]


def create_columns(column_labels):
    columns = [Header(len(column_labels))] + [Column(name=label) for label in column_labels]
    link_left_right(columns)
    return columns


def create_node_array(rows, column_labels):
    column_array = create_columns(column_labels)
