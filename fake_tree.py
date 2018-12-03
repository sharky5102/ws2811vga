import math
import json

n = 500

points = []

layer = 0
a = 0
b = 0
for i in range(0, n):
	n_per_layer = layer + 1
	l = layer / 33

	x = math.cos(a) * l
	y = math.sin(a) * l
	z = 1 - l

	points.append( (x, y, z) )
	
	a += (math.pi * 2) / n_per_layer
	b += 1
	
	if b == n_per_layer:
		b = 0
		a = 0
		layer += 1
	
print(json.dumps(points))
	