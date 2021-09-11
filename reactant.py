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


print("START")


nm=10                                                                          #Number of hours in a day
itr=100                                                                   #number of iterations

# System boundaries
Lx=pow(10,7)
Ly=pow(10,7)
Lz=1

# refractive index of particles and medium (water)
M_re=1.5837
N_re=1.33


IntensityLoss=0.05         # Fraction of intensity loss while exiting the system by a photon

# sensor coordinates
sensor_z=14.6
sensor_x=6
sensor_y=0
sensor_area=0.025

xxx=0
yyy=0

#hit coordinates
xcor=[]
zcor=[]


#0.001,0.002,0.003,0.004,0.005,0.006,0.007,0.008,0.009,0.01,0.02,0.03,0.04,0.05,0.06,0.07,0.08,0.09,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1,2,3,4,5,6,7,8,9,10,20,30,40,50,60,70,80,90,100
#-1,-0.5,-0.1,0.1,0.5,0.9,0.99,1

urange = arr.array('d',[10])

for g in [0.1] :
    #if g<xxx : continue
    for Ut in urange :
        #if g==xxx and Ut<yyy : continue

        #observations
        photon=0
        path=0
        normPath=0
        front=0
        back=0
        thru=0
        mass=0
        hit=0
        absorbWeight=0
        frequency=0

        for i in range(0,itr):

            #parameters
            Us=Ut*0.95
            Ua=Ut-Us

            if i%1000==0:
                print(i*100/itr,"%\tfor g = ",g,"\tfor Ut = ",Ut)

            # Initializing direction cosines
            Ux=0
            Uy=0
            Uz=1
            w=1       # photon weight

            # initializing coordinates
            x=0
            y=0
            z=0

            xcor.append(x)
            zcor.append(z)

            e=random.uniform(0,1)
            s=-np.log(e)/Ut          # Photon step size
            x=x+s*Ux
            y=y+s*Uy
            z=z+s*Uz
            sys=True
            lim=0

            # if photon reaches the other boundary without any interaction
            if z>Lz:
                path+=Lz
                normPath+=Lz*w
                thru+=1
                front+=1
                mass+=w
                d=abs((Lz-z)/Uz)
                z1=Lz
                x1=x/z
                y1=y/z

                xcor.append(x1)
                zcor.append(Lz)

                xo=0
                yo=0
                zo=0
                xn=0
                yn=0
                zn=Lz
                #add here 1


            # if it reaches the inlet boundary
            elif z<0:
                back+=1
                pass

            # if it undergoes scattering
            else:
                path+=s
                normPath+=s*w
                hit+=1

                xcor.append(x)
                zcor.append(z)

                xo=0
                yo=0
                zo=0
                xn=x
                yn=y
                zn=z
                #add here 2


            # While a photon is inside the system boundaries
            while 0<=z<=Lz and sys and w>0.0005:
                e=random.uniform(0,1)
                phi=e*2*3.14
        # =============================================================================
        #           e=random.uniform(0,1)
        #             for k in range(0,interval):
        #                 if zz[n][k]>e:
        #                     theta=(k*(180/interval)*(np.pi/180))
        #                     break
        # =============================================================================
                e=random.uniform(0,1)
                cos=(1/(2*g))*(1 + g**2 - ((1-g**2)/(1+g*(2*e - 1)))**2)
                theta=np.arccos(cos)
                sin_theta=np.sin(theta)
                cos_theta=np.cos(theta)
                sin_phi=np.sin(phi)
                cos_phi=np.cos(phi)
                #Updating direction cosines
                if abs(Uz)>0.99999:
                    Uz_1=np.sign(Uz)*cos_theta
                    Uy_1=sin_theta*cos_phi
                    Ux_1=sin_theta*sin_phi
                else:
                    Usqr=np.sqrt(1-Uz**2)
                    Uz_1=-sin_theta*cos_phi*Usqr + Uz*cos_theta
                    Ux_1=(sin_theta*(Uz*Ux*cos_phi - Uy*sin_phi)/(Usqr)) + Ux*cos_theta
                    Uy_1=(sin_theta*(Uz*Uy*cos_phi + Ux*sin_phi)/(Usqr)) + Uy*cos_theta
                Ux=Ux_1
                Uz=Uz_1
                Uy=Uy_1
                e=random.uniform(0,1)
                s=-np.log(e)/Ut
                loop=True
                decoy=True
                while loop:
                    z1=z+s*Uz
                    x1=x+s*Ux
                    y1=y+s*Uy
                    if 0<=z1<=Lz:

                        xo=x
                        yo=y
                        zo=z
                        xn=x1
                        yn=y1
                        zn=z1
                        #add here 3


                        x=x1
                        y=y1
                        z=z1

                        xcor.append(x)
                        zcor.append(z)

                        hit+=1
                        w=w*(1-Ua/Ut)
                        path+=s
                        normPath+=s*w
                        loop=False
                        decoy=False
                        break
                    elif z1>Lz:
                        d=abs((Lz-z)/Uz)
                        z1=Lz
                        x1=x+d*Ux
                        y1=y+d*Uy
                        path+=d
                        normPath+=d*w
                        if abs(x1)>Lx/2 or abs(y1)>Ly/2:
                            sys=False
                            loop=False
                            decoy=False
                            break

                        # Checking total internal reflection at z=1
                        # if N_re*np.sqrt(1-Uz**2)>1:
                        #     z=Lz
                        #     Uz=-Uz
                        #     s=s-d
                        #     x=x1
                        #     y=y1

                        else:
                            mass+=w
                            front+=1

                            xo=x
                            yo=y
                            zo=z
                            xn=x1
                            yn=y1
                            zn=Lz
                            #add here 4


                            x=x1
                            y=y1
                            z=z1

                            xcor.append(x)
                            zcor.append(z)

                            sys=False
                            loop=False
                            decoy=False
                            break
                            sin=(N_re/M_re)*np.sqrt(1-Uz**2)
                            Uy=Uy*(N_re/M_re)
                            Ux=Ux*(N_re/M_re)
                            norm=np.sqrt(Ux**2+Uy**2+Uz**2)
                            Ux=Ux/norm
                            Uy=Uy/norm
                            Uz=Uz/norm
                            # system has a thickness of 0.1 cm
                            d1=abs(0.1/Uz)
                            x=x + d1*Ux
                            y=y + d1*Uy
                            sin=M_re*sin
                            Uz=np.sqrt(1-sin**2)
                            Uy=(M_re)*Uy
                            Ux=(M_re)*Ux
                            norm=np.sqrt(Ux**2+Uy**2+Uz**2)
                            Ux=Ux/norm
                            Uy=Uy/norm
                            Uz=Uz/norm
                            d2=abs((sensor_z-z)/Uz)
                            x=x + d2*Ux
                            y=y + d2*Uy
                            radius=(x-sensor_x)**2+(y-sensor_y)**2
                            if radius<=sensor_area/3.14:
                                photon+=(1-IntensityLoss)
                                #print('photon= ', photon)
                            break
                    else:
                        d=abs(z/Uz)
                        path+=d
                        normPath+=d*w
                        x1=x+d*Ux
                        y1=y+d*Uy

                        xo=x
                        yo=y
                        zo=z
                        xn=x1
                        yn=y1
                        zn=0
                        #add here 5

                        z=0
                        xcor.append(x1)
                        zcor.append(z)

                        if abs(x1)>Lx/2 or abs(y1)>Ly/2:
                            sys=False
                            decoy=False
                            loop=False
                            mass+=w
                            break

                        # checking internal reflection at z=0
                        # if N_re*np.sin(np.arccos(Uz))>1:
                        #     z=0
                        #     x=x1
                        #     y=y1
                        #     s=s-d
                        #     Uz=-Uz
                        else:
                            z=z1
                            sys=False
                            loop=False
                            decoy=False
                            back+=1
                            break

                #russian roulette
                if w<0.001:
                       m=10
                       e=random.uniform(0,1)
                       if e<=1/m:
                           w=w*m
                       else:
                           w=0


print("END")
