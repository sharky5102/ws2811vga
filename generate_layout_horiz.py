#!/usr/bin/python
import math
import json

x = 50
y = 10
n = x * y
size = min(2.0 / x, 2.0 / y)

yoff = - (y * size)/2
xoff = - (x * size)/2

points = []

for i in range(0, n):
    row = i / x
    right = False if row % 2 else True

    column = i - (row * x)
    if not right:
        column = x - 1 - column
    
    points.append( (xoff + (column * size), yoff + (row * size), 0) )


print(json.dumps(points))

