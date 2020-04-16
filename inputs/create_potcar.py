import os
import sys

mat = []
for i in range(len(sys.argv)-1):
    mat.append(sys.argv[i+1])

print(mat)


catstring = 'cat '
for name in mat:
    catstring+= '/n/home02/zzhu/PPs/' + name + '_POTCAR '
    print(catstring) 
    
catstring += "> POTCAR" 

try: 
    os.system(catstring)
except: 
    print('POTCAR not found!')
