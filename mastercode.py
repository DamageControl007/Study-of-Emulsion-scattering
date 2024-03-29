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
#file_path = open("path.txt","a")
#yfile_path = open("yval.txt","a")

nm=10                                                                          #Number of hours in a day
itr=10000                                                                   #number of iterations


# Monte carlo paramters
#Ut=0.2
#Us=Ut*1
#Ua=Ut-Us
#g=0.81

# System boundaries
# Lx=1
# Ly=4.3
Lx=pow(10,7)
Ly=pow(10,7)
Lz=1

# refractive index of particles and medium (water)
M_re=1.5837
N_re=1.33


IntensityLoss=0.05         # Fraction of intensity loss while exiting the system by a photon

# Observation
"""
photon=0
path=0
front=0
back=0
thru=0
mass=0
hit=0
"""
# sensor coordinates

sensor_z=14.6
sensor_x=6
sensor_y=0
sensor_area=0.025

xxx=0
yyy=0

xcor=[]
zcor=[]
zd=[]
zp=[]
dv=100


#,1,2,3,4,5,6,7,8,9,10
#0.001,0.002,0.003,0.004,0.005,0.006,0.007,0.008,0.009,0.01,0.02,0.03,0.04,0.05,0.06,0.07,0.08,0.09,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9
#0.001,0.002,0.003,0.004,0.005,0.006,0.007,0.008,0.009,0.01,0.02,0.03,0.04,0.05,0.06,0.07,0.08,0.09,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1,2,3,4,5,6,7,8,9,10,20,30,40,50,60,70,80,90,100


urange = arr.array('d',[0.001,0.002,0.003,0.004,0.005,0.006,0.007,0.008,0.009,0.01,0.02,0.03,0.04,0.05,0.06,0.07,0.08,0.09,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1,2,3,4,5,6,7,8,9,10,20,30,40,50,60,70,80,90,100])

for g in [0] :
    #if g<xxx : continue
    for Ut in urange :
        if g==xxx and Ut<yyy : continue
        
        photon=0
        path=0
        front=0
        back=0
        thru=0
        mass=0
        hit=0

        dic=defaultdict(float)
        
        for i in range(0,itr):
            Us=Ut*0.95
            Ua=Ut-Us

            if i%100==0:
                print(i*100/itr,"%\tfor g = ",g,"\tfor Ut = ",Ut)

            # Initializing direction cosines
            Ux=0
            Uy=0
            Uz=1
            w=1       # photon weight

            e=random.uniform(0,1)

            # initializing coordinates
            x=random.uniform(-100,100)
            y=0
            z=0
            #print(x,"\t",y,"\t",z)
            #file_path.write(str(x)+"\t")
            #file_path.write(str(y)+"\t")
            #file_path.write(str(z)+"\n")
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
            if z>Lz:                                                                 #continue???
                path+=Lz
                thru+=1
                front+=1
                mass+=w
                d=abs((Lz-z)/Uz)
                z1=Lz
                x1=x/z
                y1=y/z
                """
                for j in range(int(abs((z1-0))*1000)) :
                    zcor.append(None)
                    xcor.append(None)"""

                #print(x,"\t",y,"\t",Lz)
                #file_path.write(str(x)+"\t")
                #file_path.write(str(y)+"\t")
                #file_path.write(str(Lz)+"\n")
                xcor.append(x1)
                zcor.append(Lz)

                #print(1)
                zo=0
                zn=Lz
                dor=abs(zn-zo)  #distance without scattering
                #dnw=pow((z2-z1),2) + pow((y2-y1),2) + pow((x2-x1),2)
                #dnw=pow(dnw,0.5)
                dnw=abs(s-d)
                if zo==zn:
                    zp.append(zo)
                    temp=(int(zo*dv))/dv
                    dic[temp]+=dnw
                    """while temp<=zn :
                        if temp>=zo:
                            zd.append(temp)
                        temp=temp+(1/dv)
                        temp=(int((temp+(0.01/dv))*dv))/dv"""
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

                        #if temp>=zo:
                            #zd.append(temp)
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

                        #zd.append(temp)
                        temp=temp-(1/dv)
                        temp=(int((temp+(0.01/dv))*dv))/dv
                        if temp==0:
                            #print("break")
                            break;
                zd.append(Lz)

            # if it reaches the inlet boundary
            elif z<0:                                                                   #???
                back+=1
                zd.append(0)
                pass

            # if it undergoes scattering
            else:
                path+=s
                hit+=1
                #print(x,"\t",y,"\t",z)
                #file_path.write(str(x)+"\t")
                #file_path.write(str(y)+"\t")
                #file_path.write(str(z)+"\n")
                """
                for j in range(int(abs((z-0))*1000)) :
                    zcor.append(None)
                    xcor.append(None)"""

                xcor.append(x)
                zcor.append(z)

                #print(2)
                zo=0
                zn=z
                dor=abs(zn-zo)  #distance without scattering
                #dnw=pow((z2-z1),2) + pow((y2-y1),2) + pow((x2-x1),2)
                #dnw=pow(dnw,0.5)
                dnw=abs(s)
                if zo==zn:
                    zp.append(zo)
                    temp=(int(zo*dv))/dv
                    dic[temp]+=dnw
                    """while temp<=zn :
                        if temp>=zo:
                            zd.append(temp)
                        temp=temp+(1/dv)
                        temp=(int((temp+(0.01/dv))*dv))/dv"""
                if zn>zo:
                    temp=(int(zo*dv))/dv
                    while temp<=zn :
                        if temp+(1/dv)>zn:
                            if temp>=zo:
                                dic[temp] += (zn-temp)*dnw/dor
                            else :
                                dic[temp] += (zn-zo)*dnw/dor
                        else:
                            if temp>=zo:
                                dic[temp] += (1/dv)*dnw/dor
                            else :
                                dic[temp] += (temp+(1/dv)-zo)*dnw/dor

                        #if temp>=zo:
                            #zd.append(temp)
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

                        #zd.append(temp)
                        temp=temp-(1/dv)
                        temp=(int((temp+(0.01/dv))*dv))/dv
                        if temp==0:
                            #print("break")
                            break;

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
                e=random.uniform(-1,1)
                #cos=(1/(2*g))*(1 + g**2 - ((1-g**2)/(1+g*(2*e - 1)))**2)
                #print(cos)
                cos=e
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
                        """
                        for j in range(int(abs((z1-z))*1000)) :
                            zcor.append(None)
                            xcor.append(None)"""

                        #print(3)
                        zo=z
                        zn=z1
                        dor=abs(zn-zo)  #distance without scattering
                        #dnw=pow((z2-z1),2) + pow((y2-y1),2) + pow((x2-x1),2)
                        #dnw=pow(dnw,0.5)
                        dnw=abs(s)
                        if zo==zn:
                            zp.append(zo)
                            temp=(int(zo*dv))/dv
                            dic[temp]+=dnw
                            """while temp<=zn :
                                if temp>=zo:
                                    zd.append(temp)
                                temp=temp+(1/dv)
                                temp=(int((temp+(0.01/dv))*dv))/dv"""
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

                                #if temp>=zo:
                                    #zd.append(temp)
                                temp=temp+(1/dv)
                                temp=(int((temp+(0.01/dv))*dv))/dv
                        if zn<zo:
                            temp=(int(zo*dv))/dv
                            while temp+(1/dv)>=zn:
                                #print(zo,zn)
                                #print(temp)
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

                                #zd.append(temp)
                                temp=temp-(1/dv)
                                temp=(int((temp+(0.01/dv))*dv))/dv
                                if temp==0:
                                    #print("break")
                                    break;

                        x=x1
                        y=y1
                        z=z1
                        #print(x,"\t",y,"\t",z)
                        #file_path.write(str(x)+"\t")
                        #file_path.write(str(y)+"\t")
                        #file_path.write(str(z)+"\n")
                        xcor.append(x)
                        zcor.append(z)
                        hit+=1
                        w=w*(1-Ua/Ut)
                        path+=s
                        loop=False
                        decoy=False
                        break
                    elif z1>Lz:
                        d=abs((Lz-z)/Uz)
                        z1=Lz
                        x1=x+d*Ux
                        y1=y+d*Uy
                        path+=d
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
                            """
                            for j in range(int(abs((z1-z))*1000)) :
                                zcor.append(None)
                                xcor.append(None)"""

                            #print(4)
                            zo=z
                            zn=Lz
                            dor=abs(zn-zo)  #distance without scattering
                            #dnw=pow((z2-z1),2) + pow((y2-y1),2) + pow((x2-x1),2)
                            #dnw=pow(dnw,0.5)
                            dnw=abs(d)
                            if zo==zn:
                                zp.append(zo)
                                temp=(int(zo*dv))/dv
                                dic[temp]+=dnw
                                """while temp<=zn :
                                    if temp>=zo:
                                        zd.append(temp)
                                    temp=temp+(1/dv)
                                    temp=(int((temp+(0.01/dv))*dv))/dv"""
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

                                    #if temp>=zo:
                                        #zd.append(temp)
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

                                    #zd.append(temp)
                                    temp=temp-(1/dv)
                                    temp=(int((temp+(0.01/dv))*dv))/dv
                                    if temp==0:
                                        #print("break")
                                        break;
                            zd.append(Lz)

                            x=x1
                            y=y1
                            z=z1
                            #print(x,"\t",y,"\t",z)
                            #file_path.write(str(x)+"\t")
                            #file_path.write(str(y)+"\t")
                            #file_path.write(str(z)+"\n")
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
                        """
                        for j in range(int(abs((z-0))*1000)) :
                            zcor.append(None)
                            xcor.append(None)"""

                        #print(5)
                        zo=z
                        zn=0
                        d=abs(z/Uz)
                        dor=abs(zn-zo)  #distance without scattering
                        #dnw=pow((z2-z1),2) + pow((y2-y1),2) + pow((x2-x1),2)
                        #dnw=pow(dnw,0.5)
                        dnw=abs(d)
                        if zo==zn:
                            #print(5.1)
                            zp.append(zo)
                            temp=(int(zo*dv))/dv
                            dic[temp]+=dnw
                            """while temp<=zn :
                                if temp>=zo:
                                    zd.append(temp)
                                temp=temp+(1/dv)
                                temp=(int((temp+(0.01/dv))*dv))/dv"""
                        if zn>zo:
                            temp=(int(zo*dv))/dv
                            while temp<=zn :
                                #print(5.2)
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

                                #if temp>=zo:
                                    #zd.append(temp)
                                temp=temp+(1/dv)
                                temp=(int((temp+(0.01/dv))*dv))/dv
                        if zn<zo:
                            temp=(int(zo*dv))/dv
                            while temp+(1/dv)>=zn:
                                #print(5.3)
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

                                #zd.append(temp)
                                temp=temp-(1/dv)
                                temp=(int((temp+(0.01/dv))*dv))/dv
                                if temp==0:
                                    #print("break")
                                    break;
                        zd.append(0)

                        d=abs(z/Uz)
                        z=0
                        path+=d
                        x1=x+d*Ux
                        y1=y+d*Uy
                        #print(x1,"\t",y1,"\t",z)
                        #file_path.write(str(x1)+"\t")
                        #file_path.write(str(y1)+"\t")
                        #file_path.write(str(z)+"\n")
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

        #print("I/Io at the detector=", photon/itr)
        #print("Thru=", thru/itr)
        #print("hits=", hit/itr)
        #file_path = open("data_temp.txt","a")
        
        file_path = open("g=0.txt","a")
        file_path.write(str(g)+"\t")
        file_path.write(str(Ut)+"\t")
        file_path.write(str(path/itr)+"\t")
        file_path.write(str(front/itr)+"\t")
        file_path.write(str(back/itr)+"\t")
        file_path.write(str(thru/itr)+"\t")
        file_path.write(str(hit/itr)+"\n")
        file_path.close()
        """
        file_path = open("g=0.txt","a")
        #xval=[]
        #yval=[]
        #del dic[1]
        #del dic[0]
        file_path.write("\ng="+str(g)+"\t")
        file_path.write("Ut="+str(Ut)+"\n\n")
        for key in dic:
            dic[key] = dic[key]*dv/itr
            #xval.append(key)
            file_path.write(str(key)+"\t")
            #yval.append(dic[key])
            file_path.write(str(dic[key])+"\n")
        file_path.close()"""
#file_path.close()
#print(dic)

#print(xval)
#print(yval)
#plt.plot(xval,yval)
#plt.bar(*zip(*dic.items()))
#df = pd.DataFrame(list(zip(xcor,zcor)),columns=['xcor','zcor'])
#print(df)
#print(zd)
#plt.subplot(121)
#plt.plot(df['zcor'],df['xcor'],marker=".")
#df=df.interpolate(method='linear')
#print("\n")
#print(df)
#plt.subplot(122)
#myplot = sns.kdeplot(data=df,x='zcor',cut=0,marker=".")
#sns.kdeplot(zd,cut=0,label='bw_adjust=1')
#sns.kdeplot(data=df,x='zcor',y='xcor',cmap="seismic",fill=True,cbar=True,cut=0)
#sns.displot(zd,binwidth=0.005,stat="count")
#plt.plot(itr)
#plt.axhline(y = itr, color = 'r', linestyle = '-',xmin=0,xmax=1)
#sns.displot(zd,binwidth=0.001,stat="probability")
#sns.displot(zd,binwidth=0.02,stat="probability")
#sns.displot(zd,binwidth=0.001,stat="count")
#sns.displot(zp,binwidth=0.02,stat="count")
#sns.displot(zd,binwidth=0.1,stat="count")
"""
dataset = myplot.get_lines()[0].get_data()
data = pd.DataFrame(dataset).transpose()
#print(data)

with file_path as f:
    dfAsString = data.to_string(header=False, index=False)
    f.write(dfAsString)
"""
#file_path.write(dataset)
#plt.xlabel('z-coordinate')
#plt.ylabel('Residence time')
#plt.title("Plot depicting photon residence time\ng = "+str(g)+" & Ut = "+str(Ut)+"\nitr = "+str(itr)+"\ndiv = "+str(dv))
#plt.xlim(0,1)
#plt.ylim(0,15000)
#plt.subplot(122)
#plt.plot(df['zcor'],df['xcor'],marker=".")
#plt.legend()
#plt.show()
#print(dic)

print("END")

# =============================================================================
# with open(heading + '_'+ wavelength + ' nm'+".csv", 'w', newline='') as f:
#     thewriter=csv.writer(f)
#     thewriter.writerow(['Normalised weigth L/Lo vs volume fraction'])
#     thewriter.writerow(['wavelength'])
#     thewriter.writerow([ wavelength])
#     thewriter.writerow(['Time', 'I/Io', 'backscattering','pm2.5','PBLH', 'UtxLo'])
#     for i in range(0,nm):
#         thewriter.writerow([time[i], weight[i], knight[i], pm[i], boun[i], UtxLo[i]])
# =============================================================================
