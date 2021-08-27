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

print("START CODE")
for g in [-0.9,-0.5,-0.1]:
    x=[]
    itr=1000000
    for i in range(0,itr):
        e=random.uniform(0,1)
        cos=(1/(2*g))*(1 + g**2 - ((1-g**2)/(1+g*(2*e - 1)))**2)
        x.append(cos)
    """
    file_path = open("cos.txt","a")
    file_path.write(str(g)+"\t")
    file_path.write(str(x/itr)+"\n")
    file_path.close()"""
    #print("START PLOT 1")
    #sns.displot(x,stat="probability")
    #print("START PLOT 2")
    #sns.displot(x,stat="probability",binwidth=0.01)
    print("START PLOT")
    sns.kdeplot(x,label=g)
    print("END PLOT")
plt.xlim(-1,1)
plt.title("cos distribution"+"\nitr = "+str(itr))
plt.xlabel('cos')
#plt.ylabel('probability')
plt.legend()
plt.show()
print("END CODE")