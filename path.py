#!/usr/bin/env python
# PATH DATA
path = []

# bottom row
path += [loc( 6, 6, 0)]
path += [loc(10, 6, 0)]
path += [loc(22, 6, 0)]
path += [loc(26, 6, 0)]
path += [loc(30, 6, 0)]

# middle row
path += [loc(30,18,pi)]
path += [loc(26,18,pi)]
path += [loc(14,18,pi)]
path += [loc(10,18,pi)]
path += [loc( 6,18,pi)]

# top row
path += [loc( 6,30, 0)]
path += [loc(10,30, 0)]
path += [loc(22,30, 0)]
path += [loc(26,30, 0)]
path += [loc(30,30, 0)]

pathPts = len(path)
