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
from colorspacious import cspace_converter
from collections import OrderedDict
from collections import defaultdict

def grid_index(x,y,z):
	
	dv=100
	r=pow(x*x+y*y,0.5)

	#z-index
	zi=(int(z*dv)) + 1
	if z=0:
		zi=0
	
	#r-index
	ri=(int(r*dv))

	return ri,zi;

def make_grid(df):

	#initializing 2d array
	grid=np.zeros((1000,110))
	
	for i in range(len(df)):
		x=df.loc[i,"xcor"]
		y=df.loc[i,"ycor"]
		z=df.loc[i,"zcor"]
		w=df.loc[i,"wl"]
		ri,zi=grid_index(x,y,z)
		
		grid[ri,zi]+=w