# euler-tiles
Project to investigate polyominoes whose outline has an Euler path.  A
collaboration with Jay Schindler and Glenn Hurd.  Tiles are expressed as lists
of strings of equal lengths.  The code makes the assumption that there are no
completely blank columns and no completely blank rows.  Each tile has eight
possible orientations, but the methods here remove any of these which are
identical.

The near-term goal is to determine whether a given set of tiles can fit into a
specified area also expressed as a list of strings, however later
investigations can include generating all possible tiles with a fixed number
of squares.
