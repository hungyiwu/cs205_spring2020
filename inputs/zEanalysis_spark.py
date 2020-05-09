# ziyan zhu
# analyze z vs E data
# find ground state energy
from pyspark import SparkConf, SparkContext, SQLContext
from pyspark.sql.functions import lit
import string
import sys
import matplotlib.pyplot as plt
import numpy as np
import re
from pymatgen.core.periodic_table import *

plt.rcParams.update({'font.size': 22})
fpath = "../results/"

def parser(lines):
    type = line[0]

    # get atom names
    a=re.search("alignment",type)
    i1=a.span()[0]
    atom_list=type[0:i1-1]
    atoms=atom_list.split("_")
    a1=re.findall('[A-Z][^A-Z]*',atoms[0])
    a2=re.findall('[A-Z][^A-Z]*',atoms[1])
    a1_l1=a1[0]
    a2_l1=a2[0]
    a1_l2=a1[1]
    a2_l2=a2[1]

    # get aligntments
    b=re.search("0",type)
    align=type[b.span()[0]:]
    alignment = align.split("_")[1]
    return a1_l1,a2_l1,a1_l2,a2_l2,alignment


try:
    chalcogen1 = sys.argv[1]
    chalcogen2 = sys.argv[2]
    align = sys.argv[3]
except:
    chalcogen1 = 'Te'
    chalcogen2 = 'Te'
    align = '0'

# organize zElist
f = open("zElist.txt","r")
f2 = open("zElist_organized.txt","w+")
f2.write("atom1_l1,atom2_l1,atom1_l2,atom2_l2,orientation,z,E0\n")

f3 = open("zoptlist.txt","r")
f4 = open("zoptlist_organized.txt","w+")
f4.write("atom1_l1,atom2_l1,atom1_l2,atom2_l2,orientation,z\n")

for lines in f:
    line = re.split(",",lines)
    a1_l1,a2_l1,a1_l2,a2_l2,alignment=parser(line)
    z = line[1]
    E0 = line[2]

    f2.write(a1_l1+","+a2_l1+","+a1_l2+","+a2_l2+","+alignment+","+z+","+E0)

for lines in f3:
    line = re.split(",",lines)
    z = line[1]
    a1_l1,a2_l1,a1_l2,a2_l2,alignment=parser(line)
    f4.write(a1_l1+","+a2_l1+","+a1_l2+","+a2_l2+","+alignment+","+z)

f.close()
f2.close()
f3.close()
f4.close()

conf = SparkConf().setMaster('local[2]').setAppName('zE')
sqlContext = SQLContext(SparkContext())

df_full = sqlContext.read.csv("zElist_organized.txt",header=True)
df_full.persist()

df = sqlContext.read.csv("zoptlist_organized.txt",header=True)
df.persist()

# find unique metals
metal_l1=df_full.select("atom1_l1").distinct()
metal_l2=df_full.select("atom1_l2").distinct()


metal_l1_list = [x["atom1_l1"] for x in metal_l1.collect()]
metal_l2_list = [x["atom1_l2"] for x in metal_l2.collect()]

Z1 = [Element(x).Z for x in metal_l1_list]
Z2 = [Element(x).Z for x in metal_l2_list]

idx1 = np.argsort(Z1)
idx2 = np.argsort(Z2)

# go through the list of metals and do a fit
E0 = np.zeros([len(metal_l1_list),len(metal_l2_list)])
z = np.zeros([len(metal_l1_list),len(metal_l2_list)])
zarr=np.linspace(3.6,5.56,500)
plt.figure(figsize=(20,15))
for i in range(len(metal_l1_list)):
    for j in range(len(metal_l2_list)):

        entry=df_full.filter(df_full["atom1_l1"]==metal_l1_list[i]).filter(df_full["atom1_l2"]==metal_l2_list[j]).filter(df_full["atom2_l1"]==chalcogen1).filter(df_full["atom2_l2"]==chalcogen2).filter(df_full["orientation"]==align)
        combo = metal_l1_list[i]+chalcogen1+"+"+metal_l2_list[i]+chalcogen2
        
        if entry.count() > 0:
            E_list = [float(x["E0"]) for x in entry.collect()]
            z_list = [float(x["z"]) for x in entry.collect()]
            
            # fit
            p=np.polyfit(z_list,E_list,10)
            fit=np.poly1d(p)
            earr=fit(zarr)
            ind=np.argmin(earr)
            z[i,j]=zarr[ind]
            E0[i,j]=earr[ind]
            if z[i,j]==5.56 or np.max(earr-np.min(earr))>1:
                E0[i,j]=None
                z[i,j]=None
            else:
                # plt.plot(zarr,earr-np.min(earr),label=combo + " fit")
                plt.plot(z_list,E_list-np.min(E_list),'o-',label=combo)
                plt.plot(zarr[ind],0,'x',color=plt.gca().lines[-1].get_color(),markersize=8)
                plt.xlabel("z (A)")
                plt.ylabel("E0 (eV)")
                

        else:
            E0[i,j]=None
            z[i,j]=None

# sort by atomic number
E0=E0[idx1,:]
E0=E0[:,idx2]
z=z[idx1,:]
z=z[:,idx2]
Z1=np.sort(Z1)
Z2=np.sort(Z2)

metal1z=[metal_l1_list[x]+"("+str(Z1[x])+")" for x in range(len(Z1))]
metal2z=[metal_l2_list[x]+"("+str(Z2[x])+")" for x in range(len(Z2))]
            
plt.legend()
plt.savefig(fpath+"E0_vs_z_"+chalcogen1+chalcogen2+"_"+align+".png")
        
fig=plt.figure(figsize=(20,15))
im=plt.pcolormesh(E0)
fig.colorbar(im)
plt.yticks(np.arange(len(metal_l1_list)), tuple(metal1z))
plt.xticks(np.arange(len(metal_l2_list)), tuple(metal2z))
plt.title("Chalcogen L1: " + chalcogen1 + ", Chalcogen L2: " + chalcogen2)
plt.xlabel("Metal L1")
plt.ylabel("Metal L2")
plt.savefig(fpath+"E0_"+chalcogen1+chalcogen2+"_"+align+".png")

fig=plt.figure(figsize=(20,15))
im=plt.pcolormesh(z)
fig.colorbar(im)
plt.yticks(np.arange(len(metal_l1_list)), tuple(metal1z))
plt.xticks(np.arange(len(metal_l2_list)), tuple(metal2z))
plt.title("Chalcogen L1: " + chalcogen1 + ", Chalcogen L2: " + chalcogen2)
plt.xlabel("Metal L1")
plt.ylabel("Metal L2")
plt.savefig(fpath+"z_"+chalcogen1+chalcogen2+"_"+align+".png")
