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

def grid_index(x,z):

	dv=100

	#z-index
	zi=(int(z*dv)) + 1
	if z==0:
		zi=0

	#x-index
	xi=(int(x*dv))

	return xi,zi;

def make_grid(df):

	#initializing 2d array
	grid=np.zeros((1001,102))

	for i in range(len(df)):
		x=df.loc[i,"xcor"]
		z=df.loc[i,"zcor"]
		w=df.loc[i,"wl"]
		xi,zi=grid_index(x,z)

		xi=xi+500
		if xi>1000 or xi<0: continue
		grid[xi,zi]+=w

	#making meshgrid
	tx=np.arange(102)
	tx=tx-1
	tx=tx/100
	tx=tx+0.005
	ty=np.arange(-500,500)
	ty=ty/100
	ty=ty+0.005
	xx, yy = np.meshgrid(tx,ty)

	plt.contourf(xx,yy,grid,cmap="jet",levels=100)
	plt.colorbar()
	#plt.axis('equal')
	#plt.ylim(0.005,0.02)
	plt.show()
