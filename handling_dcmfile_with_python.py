#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd


# In[ ]:


dfi = pd.read_excel('Your_File_Name.xlsx',header=0)


# In[ ]:


dfi


# In[ ]:


str_array = []
temp_str = ''

for i in range(0,len(dfi)):
    raw_value = dfi.iloc[i].Name
        
    if('FESTWERT' in str(raw_value)):
        actual_fest = raw_value.split(' ')[1]
        temp_str = str(actual_fest)
        
    elif('LANGNAME' in str(raw_value)):
        actual_langname = raw_value.split('LANGNAME')[1]
        temp_str = str(temp_str) + ','+ str(actual_langname)
        
    elif('EINHEIT_W' in str(raw_value)):
        actual_einheit = raw_value.split('EINHEIT_W')[1]
        temp_str = str(temp_str) + ','+ str(actual_einheit)
        
    elif('WERT' in str(raw_value)):
        actual_wert = raw_value.split('WERT')[1]
        #'print(actual_wert)'
        temp_str = str(temp_str) + ','+ str(round(float(actual_wert), 4))
        
    if('END' in str(raw_value)):
        temp_str = temp_str.replace(" ","")
        str_array.append(temp_str.lstrip())
        
        


# In[ ]:


df = pd.DataFrame(data=str_array, index=None, columns=['column1'])
df = df.column1.str.split(',',expand=True)
df.columns=['FESTWERT','LANGNAME','EINHEIT_W', 'WERT']
df['WERT'] = pd.to_numeric(df['WERT'])
df.to_csv('dcmfile_python_.txt',sep =';')		#'dcmfile_python' this name of file you will find in your folder 
df


# In[ ]:




