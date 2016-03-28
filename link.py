"""Implementation of Knuth's Link Class."""


class Link:
    """Knuth's Link class corresponding to ones in an exact cover matrix.
    """

    def __init__(self, left=None, right=None, up=None, down=None, column=None):
        self.Left = left
        self.Right = right
        self.Up = up
        self.Down = down
        self.Column = column
