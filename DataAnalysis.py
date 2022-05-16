import numpy as np
import pandas as pd

File='DataFile_g01_Ut1.csv'
df=pd.read_csv(File)
print(df)
df=df.to_numpy()
print(df[3][1])