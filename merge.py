'''
import pandas as pd
import os, glob3

os.chdir('C:\\Users\\Shadman\\Desktop\\Coding\\Python Projects\\recursion\\combine')

dfs = [pd.read_csv(f, index_col=[0], parse_dates=[0])
        for f in os.listdir(os.getcwd()) if f.endswith('csv')]

finaldf = pd.concat(dfs, axis=1, join='inner').sort_index()
'''

