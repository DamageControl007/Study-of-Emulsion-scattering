import numpy

def next_point(x, y, z, Ux, Uy, Uz, s):
	x=x+Ux*s
	y=y+Uy*s
	z=z+Uz*s
	return x,y,z