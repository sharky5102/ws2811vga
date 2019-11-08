import math
import json

x = 32
y = 8
n = x * y
size = min(2.0 / x, 2.0 / y)

yoff = - (y * size)/2
xoff = - (x * size)/2

points = []

for i in range(0, n):
    column = i / y
    down = False if column % 2 else True

    row = i - (column * y)
    if not down:
        row = y - 1 - row

    points.append( (xoff + (column * size), yoff + (row * size), 0) )


print(json.dumps(points))

