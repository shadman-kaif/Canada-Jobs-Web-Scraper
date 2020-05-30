# import numpy as np
import pandas as pd
import glob

#### Combine, concatenate, join multiple excel files in a given folder into one dataframe, Each excel files having multiple sheets
#### All sheets in a single Excel file are first combined into a dataframe, then all the Excel Books in the folder
#### Are combined to make a single data frame. The combined data frame is the exported into a single Excel sheet.

# path = r'C:\Users\Tchamna\Downloads\UTRC_DATA\495GowanusSpeedData20152016'
path = r"C:\Users\KhanAbd\OneDrive - Government of Ontario\Desktop"

filenames = glob.glob(path + "/*.xlsx")
print(filenames)

### Dataframe Initialization
concat_all_sheets_all_files = pd.DataFrame()

for file in filenames:
    ### Get all the sheets in a single Excel File using  pd.read_excel command, with sheet_name=None
    ### Note that the result is given as an Ordered Dictionary File
    ### Hell can be found here: https://pandas.pydata.org/pandas-docs...

    df = pd.read_excel(file, sheet_name=None, skiprows=None, nrows=None, usecols=None, header=0, index_col=None)
    # df = pd.read_excel(file, sheet_name=None, skiprows=0,nrows=34,usecols=105,header = 9,index_col=None)

    # print(df)

    ### Use pd.concat command to Concatenate pandas objects as a Single Table.
    concat_all_sheets_single_file = pd.concat(df, sort=False)

    ### Use append command to append/stack the previous concatenated data on top of each other
    ### as the iteration goes on for every files in the folder

    concat_all_sheets_all_files = concat_all_sheets_all_files.append(concat_all_sheets_single_file)
    # print(concat_all_sheets)

writer = pd.ExcelWriter(r"C:\Users\KhanAbd\OneDrive - Government of Ontario\Desktop\master_file.xlsx")
concat_all_sheets_all_files.to_excel(writer)
writer.save()
