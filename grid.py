import numpy as np
import random
import array as arr
import matplotlib.pyplot as plt
import miepython as mp
import csv
import xlrd
import xlsxwriter
import sys
from datetime import date
from pysolar.solar import *
import datetime
from solarpy import irradiance_on_plane
import seaborn as sns
import pandas as pd
from matplotlib import cm
from matplotlib import ticker
from colorspacious import cspace_converter
from collections import OrderedDict
from collections import defaultdict

def grid_index(x,y,z):
	
	dv=100
	r=pow(x*x+y*y,0.5)

	#z-index
	zi=(int(z*dv)) + 1
	if z==0:
		zi=0
	
	#r-index
	ri=(int(r*dv))

	return ri,zi;

def make_grid(df):

	#initializing 2d array
	grid=np.zeros((101,102))
	
	for i in range(len(df)):
		x=df.loc[i,"xcor"]
		y=df.loc[i,"ycor"]
		z=df.loc[i,"zcor"]
		w=df.loc[i,"wl"]
		ri,zi=grid_index(x,y,z)
		
		if ri>100: continue
		grid[ri,zi]+=w

	#making meshgrid
	tx=np.arange(102)
	tx=tx-1
	tx=tx/100
	tx=tx+0.005
	ty=np.arange(101)
	ty=ty/100
	ty=ty+0.005
	xx, yy = np.meshgrid(tx,ty)

	plt.contourf(xx,yy,grid,cmap="jet")
	plt.colorbar()
	#plt.axis('equal')
	#plt.ylim(0.005,0.02)
	plt.show()