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

def zip(z1,z2,dnw):
	zo=0 #z1
    zn=Lz #z2
    dor=abs(zn-zo)
    dnw=abs(s-d) #input
    if zo==zn:
        temp=(int(zo*dv))/dv
        return dnw
    if zn>zo:
        temp=(int(zo*dv))/dv
        while temp<=zn :
            if temp+(1/dv)>zn:
                if temp>=zo:
                    return (zn-temp)*dnw/dor
                else :
                    return (zn-zo)*dnw/dor
            else:
                if temp>=zo:
                    return (1/dv)*dnw/dor
                else :
                    return (temp+(1/dv)-zo)*dnw/dor
            temp=temp+(1/dv)
            temp=(int((temp+(0.01/dv))*dv))/dv
    if zn<zo:
        temp=(int(zo*dv))/dv
        while temp+(1/dv)>=zn:
            if temp+(1/dv)>zo:
                if temp<=zn:
                    return (zo-zn)*dnw/dor
                else:
                    return (zo-temp)*dnw/dor
            else:
                if temp<zn:
                    return (temp+(1/dv)-zn)*dnw/dor
                else:
                    return (1/dv)*dnw/dor
            temp=temp-(1/dv)
            temp=(int((temp+(0.01/dv))*dv))/dv
            if temp==0:
                break;

def xip(x1,x2,dnw):
	zo=x1
    zn=x2
    dor=abs(zn-zo)  #distance without scattering
    dnw=abs(s-d) #input
    if zo==zn:
        temp=(int(zo*dv))/dv
        return dnw
    if zn>zo:
        temp=(int(zo*dv))/dv
        while temp<=zn :
            if temp+(1/dv)>zn:
                if temp>=zo:
                    return (zn-temp)*dnw/dor
                else :
                    return (zn-zo)*dnw/dor
            else:
                if temp>=zo:
                    return (1/dv)*dnw/dor
                else :
                    return (temp+(1/dv)-zo)*dnw/dor
            temp=temp+(1/dv)
            temp=(int((temp+(0.01/dv))*dv))/dv
    if zn<zo:
        temp=(int(zo*dv))/dv
        while temp+(1/dv)>=zn:
            if temp+(1/dv)>zo:
                if temp<=zn:
                    return (zo-zn)*dnw/dor
                else:
                    return (zo-temp)*dnw/dor
            else:
                if temp<zn:
                    return (temp+(1/dv)-zn)*dnw/dor
                else:
                    return (1/dv)*dnw/dor
            temp=temp-(1/dv)
            temp=(int((temp+(0.01/dv))*dv))/dv
            if temp==0:
                break;

def next_point(x, y, z, Ux, Uy, Uz, s):
    x=x+Ux*s
    y=y+Uy*s
    z=z+Uz*s
    return x,y,z

def update(z1,z2,x1,x2,dnw,wo):
	s=min(zip(z1,z2,dnw),xip(x1,x2,dnw))
	wn=wo*(pow(2.718,beta*s)) #weight update
	#point inside grid, 
	#add energy to grid
	#new point, z1n,x1n
	dnw=dnw-s

def insert()