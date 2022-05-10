#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 20 11:35:00 2022

@author: somendrasinghjadon
"""

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd



var1 = pd.read_excel("Absorption_Files/DataFile_g01_abs05.xlsx")
var2 = pd.read_excel("Absorption_Files/DataFile_g03_abs05.xlsx")
var3 = pd.read_excel("Absorption_Files/DataFile_g05_abs05.xlsx")
var4 = pd.read_excel("Absorption_Files/DataFile_g07_abs05.xlsx")
var5 = pd.read_excel("Absorption_Files/DataFile_g09_abs05.xlsx")

var6 = pd.read_excel("Absorption_Files/DataFile_g01_abs1.xlsx")
var7 = pd.read_excel("Absorption_Files/DataFile_g03_abs1.xlsx")
var8 = pd.read_excel("Absorption_Files/DataFile_g05_abs1.xlsx")
var9 = pd.read_excel("Absorption_Files/DataFile_g07_abs1.xlsx")
var10 = pd.read_excel("Absorption_Files/DataFile_g09_abs1.xlsx")

var11 = pd.read_excel("Absorption_Files/DataFile_g01_abs3.xlsx")
var12 = pd.read_excel("Absorption_Files/DataFile_g03_abs3.xlsx")
var13 = pd.read_excel("Absorption_Files/DataFile_g05_abs3.xlsx")
var14 = pd.read_excel("Absorption_Files/DataFile_g07_abs3.xlsx")
var15 = pd.read_excel("Absorption_Files/DataFile_g09_abs3.xlsx")

var16 = pd.read_excel("Absorption_Files/DataFile_g01_abs5.xlsx")
var17 = pd.read_excel("Absorption_Files/DataFile_g03_abs5.xlsx")
var18 = pd.read_excel("Absorption_Files/DataFile_g05_abs5.xlsx")
var19 = pd.read_excel("Absorption_Files/DataFile_g07_abs5.xlsx")
var20 = pd.read_excel("Absorption_Files/DataFile_g09_abs5.xlsx")

var21 = pd.read_excel("Absorption_Files/DataFile_g01_abs0.xlsx")
var22 = pd.read_excel("Absorption_Files/DataFile_g03_abs0.xlsx")
var23 = pd.read_excel("Absorption_Files/DataFile_g05_abs0.xlsx")
var24 = pd.read_excel("Absorption_Files/DataFile_g07_abs0.xlsx")
var25 = pd.read_excel("Absorption_Files/DataFile_g09_abs0.xlsx")

# =============================================================================
# var1 = pd.read_excel("No_absorption/DataFile_g01_abs0.xlsx")
# var2 = pd.read_excel("No_absorption/DataFile_g03_abs0.xlsx")
# var3 = pd.read_excel("No_absorption/DataFile_g05_abs0.xlsx")
# var4 = pd.read_excel("No_absorption/DataFile_g07_abs0.xlsx")
#var5 = pd.read_excel("No_absorption/DataFile_g09_abs0_ver2.xlsx")
# =============================================================================

# =============================================================================
# x = list(var1['Interaction coefficient'])
# x2 = list(var2['Interaction coefficient'])
# y1 = list(var1['Weight norm L/L0'])
# y2 = list(var1['Collisions'])
# y3 = list(var1['Backscattered'])
# y4 = list(var1['Front'])
# y5 = list(var5['Avg max z coordinate'])
# =============================================================================
x = list(var1['Interaction coefficient'])
x2 = list(var1['Interaction coefficient'])
y1 = list(var1['Weight norm L/L0'])
y2 = list(var5['Weight norm L/L0'])
#y3 = list(var18['Weight norm L/L0'])
#y4 = list(var19['Weight norm L/L0'])
#y5 = list(var20['Weight norm L/L0'])



plt.figure(figsize=(10,10), linewidth=2)
plt.style.use('seaborn')


plt.plot(np.log10(x2), y1, 'b-', label=r"$g=0.1$")
plt.plot(np.log10(x2), y2, 'r-', label=r"g=0.3")
#plt.plot(np.log10(x2), y3, 'g-', label=r"$g=0.5$")
#plt.plot(np.log10(x2), y4, 'm-', label=r"$g=0.7$")
#plt.plot(np.log10(x2), y5, 'c-', label=r"$g=0.9$" )
# =============================================================================
# plt.plot(np.log10(x),y1,'b-', label=r"$g=0.1$")
# plt.plot(np.log10(x),y2,'r-', label=r"$g=0.3$")
# plt.plot(np.log10(x),y3,'g-', label=r"Backscattered")
# plt.plot(np.log10(x),y4,'m-', label=r"Front")
# plt.plot(np.log10(x),y5,'k-', label=r"Avg max z coordinate")
# =============================================================================
#plt.title("Figure 2", fontsize=22)

plt.grid(False)


plt.xlabel(r"$Log_{10}(\mu_t')$", fontsize=22)
plt.ylabel(r"$L/L_0$", fontsize=22)
txt=r"Comparision of photon mass after exiting for different values of $\mu_a$ at constant $g=0.1$ is shown in the above figure."
#txt=r"Figure 1: Weight normaized $\frac{L}{L_0}$ values are plotted against log of $\mu_t$ for different values of $g$. Absroption factor $\mu_a=0$"
#plt.figtext(0.5, 0.01, txt, wrap=True, horizontalalignment='center', fontsize=16)
plt.legend(bbox_to_anchor =(1, 0.5), loc='center left')
plt.plot()
plt.show()