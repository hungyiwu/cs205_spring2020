# ziyan zhu
# find entries matching user input materials
# arguments: metal, chalcogen, alignment, number of cores to use
from pyspark import SparkConf, SparkContext, SQLContext
from pyspark.sql.functions import lit
import string
import sys
import matplotlib.pyplot as plt
import numpy as np
import re
from pymatgen.core.periodic_table import *

try:
    metal1 = sys.argv[1]
    chalcogen1 = sys.argv[2]
    align = sys.argv[3]
    np = sys.argv[4]
except:
    print("One or more input arguments missing!")

conf = SparkConf().setMaster('local[1]').setAppName('zE')
sqlContext = SQLContext(SparkContext())

df_full = sqlContext.read.csv("zElist_organized.txt",header=True)
df_full.persist()
df_full.show()

# find all entries with
entry=df_full.filter(df_full["atom1_l1"]==metal1).filter(df_full["atom2_l1"]==chalcogen1).filter(df_full["orientation"]==align)

entry.show()

entry.write.csv('output')
