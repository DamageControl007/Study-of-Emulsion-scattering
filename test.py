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
import grid
import random

xcor=[]
ycor=[]
zcor=[]
wl=[]

x=0

rc=5

for i in range(0,100000):
	xcor.append(random.uniform(rc-1, rc+1))
	ycor.append(0)
	zcor.append(random.uniform(0,1))
	wl.append(1)



# while x<1 :
# 	xcor.append(x)
# 	ycor.append(x)
# 	zcor.append(x)
# 	wl.append(1)
# 	x=x+0.01
#
# for i in range(1,10):
# 	xcor.append(0.5)
# 	ycor.append(0.5)
# 	zcor.append(0.8)
# 	wl.append(1)

df1 = pd.DataFrame(list(zip(xcor,ycor,zcor,wl)),columns =['xcor','ycor','zcor','wl'])
grid.make_grid(df1)
