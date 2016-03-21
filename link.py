"""Implementation of Knuth's Link Class."""


class Link:
    """Knuth's Link class corresponding to ones in an exact cover matrix.
    """

    def __init__(self):
        self.Left = None
        self.Right = None
        self.Up = None
        self.Down = None
        self.Column
