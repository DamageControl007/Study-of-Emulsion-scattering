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

def yip():
	zo=0
    zn=Lz
    dor=abs(zn-zo)  #distance without scattering
    dnw=abs(s-d)
    dnw=dnw*w
    if zo==zn:
        temp=(int(zo*dv))/dv
        dic[temp]+=dnw
    if zn>zo:
        temp=(int(zo*dv))/dv
        while temp<=zn :
            if temp+(1/dv)>zn:
                if temp>=zo:
                    dic[temp]+=(zn-temp)*dnw/dor
                else :
                    dic[temp]+=(zn-zo)*dnw/dor
            else:
                if temp>=zo:
                    dic[temp]+=(1/dv)*dnw/dor
                else :
                    dic[temp]+=(temp+(1/dv)-zo)*dnw/dor
            temp=temp+(1/dv)
            temp=(int((temp+(0.01/dv))*dv))/dv
    if zn<zo:
        temp=(int(zo*dv))/dv
        while temp+(1/dv)>=zn:
            if temp+(1/dv)>zo:
                if temp<=zn:
                    dic[temp]+=(zo-zn)*dnw/dor
                else:
                    dic[temp]+=(zo-temp)*dnw/dor
            else:
                if temp<zn:
                    dic[temp]+=(temp+(1/dv)-zn)*dnw/dor
                else:
                    dic[temp]+=(1/dv)*dnw/dor
            temp=temp-(1/dv)
            temp=(int((temp+(0.01/dv))*dv))/dv
            if temp==0:
                break;