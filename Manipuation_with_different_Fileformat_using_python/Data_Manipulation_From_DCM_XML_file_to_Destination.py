#!/usr/bin/env python
# coding: utf-8

# In[1]:


############### We may need certain Libraries ###############

import pandas as pd
import numpy as np 
import csv 
import copy


# In[2]:


############### Start --> working with .dcm File ###############

############### Goal 1 : Here in this original Dcm file,we want only FESTWERT(FESTWERT OR LANGNAME ###############
############### -Because both strings are same) & WERT.                                            ###############
############### Goal 2 : WE want to remove unnecessory words(Like C_AdaPa_ & _f32) from FESTWERT   ###############


define_dcm=open("ADA_default_mod_C03.dcm","r+")            
rdcm=define_dcm.read()
dcmfile = rdcm.split('\n')
#dcmfile


# In[3]:


str_array = []
temp_str = ""

for i in range(0,len(dcmfile)):
    temp=dcmfile[i]
    #print(i,temp)
    
    if "FESTWERT " in str(temp):
        actual_Festwert= str(temp).split("FESTWERT ")[1]
        name = str(actual_Festwert)[8:-3]
        temp_str = str(name)
        #print("FESTWERT1 IS BEING PRINTED", temp_str)
        
        if('_' in str(name)):
            actual_name= name[:-1]
            temp_str = str(actual_name)
            #print("FESTWERT2 IS BEING PRINTED", temp_str)
            
#     if "LANGNAME " in str(temp):
#         actual_langname = str(temp).split('LANGNAME ')[1]
#         name = str(actual_langname)[9:-5]
#         temp_str = str(temp_str) + ','+ str(name)
#         #print("Langname IS BEING PRINTED", temp_str)
#        
#     if "EINHEIT_W " in str(temp):
#         actual_einheit = temp.split('EINHEIT_W ')[1]
#         temp_str = str(temp_str) + ','+ str(actual_einheit)
#         #print("einheit IS BEING PRINTED", temp_str)
        
    if "WERT   " in str(temp):
        if"   48   51   48   49" in str(temp):
            #print("i am inside if-----------------------")
            actual_wert = temp.split('WERT')[1]
            #print("actual_wert",actual_wert)
            temp_str = str(temp_str) + ','+ str(actual_wert)
        else:
            actual_wert = temp.split('WERT')[1]
            #print("inside else::::::::: actual_wert",actual_wert)
            temp_str = str(temp_str) + ','+ str(round(float(actual_wert), 4))
            #print("WERT IS BEING PRINTED", temp_str)
            
    if'END' in str(temp):
        str_array.append(temp_str.split(","))
        
#print(str_array[0:20])


# In[4]:


df = pd.DataFrame(data=str_array[3:260], index=None, columns=['Name','Value'])
df.to_csv('1_dcm_file_data.csv',sep =';')
#df

############### End --> working with .dcm File ###############


# In[5]:


############### Start --> working with .xml File ###############

############### Goal 1 : Here in this original Xml file,we want only "ConfigVariable name & Value" ###############
############### Goal 2 : WE want to remove unnecessory words(Like "AdaAlgo_Get") from FESTWERT     ###############

define_xml=open("ConfigVariables.xml","r+")            
rxml=define_xml.read()
xmlfile = rxml.split('\n')
#xmlfile


# In[6]:


str_array = []
temp_str = ""

for i in range(0,len(xmlfile)):
    temp=xmlfile[i]
    #print(i,temp)
    
    if "<ConfigVariable name=" in str(temp):
        actual_name= str(temp).split("<ConfigVariable name=")[1]
        name= str(actual_name).split(" ")[0]
        name = str(name)[1:-1]
        #print("checked name",name)
        name= str(name)[11:]
        #print("deleted unwanted Letter",name)
        
        actual_value= str(actual_name).split("value=")[1]
        #print("checked value",actual_value)
        value= actual_value[1:-2]
        
        temp_str = str(name)+ ','+ str(value)
        #print("name & Value is being printed",temp_str)
        
#     if "<id>" in str(temp):
#         actual_id= str(temp).split("<id>")[1]
#         id= str(actual_id).split("</id>")[0]
#         temp_str = str(temp_str) +','+ str(id)
        
    if "</ConfigVariable>" in str(temp):
        str_array.append(temp_str.split(","))
        
#print(str_array[130:145])


# In[7]:


df = pd.DataFrame(data=str_array, index=None, columns=['ADTF_Name','Value'])
df.to_csv('2_xml_file_data.csv',sep =';')
#df

############### End --> working with .xml File ###############


# In[8]:


############### Start --> .dcm & .xml in one File ###############

############### Goal 1 : Here, we want to create one File Data from two different File Data        ###############

filenames = ['1_dcm_file_data.csv', '2_xml_file_data.csv']

with open('3_dcm&xml_in_one_file.csv','w') as outfile:
    for names in filenames:
        with open(names) as infile:
            outfile.write(infile.read())
            
        outfile.write("\n")
        
############### End --> .dcm & .xml in one File ###############


# In[9]:


############### Start --> Filteration of .dcm & .xml ###############

############### Goal 1 : Here we want to use the same Name from dcm & xml Data and use their name&Value     ###############
############### Goal 2 : If there are no same name then use the name of only xml Data                       ###############
############### Goal 3 : same Name & Value Data with their Indexing has to be printed first for Visualation ###############
############### Goal 3 : and Other data has to be printed afterword                                         ###############

ofile=open('3_dcm&xml_in_one_file.csv',"r+")
rfile= ofile.read()
sfile=rfile.split('\n')
dcmfile= sfile[:257]
#dcmfile
#print("Length of Dcm_name:",len(dcmfile))
xmlfile= sfile[258:]
#xmlfile
#print("Length of ADTF_name:",len(xmlfile))

#print("difference of Length: ",len(xmlfile)-len(dcmfile))


# In[10]:


with open('4_Filteration_of_dcm_and_xml.csv', 'w+') as ffile:
    for i in copy.copy(xmlfile):
        XML_row_values = i.split(';')
        #print("I am in the XML File:",XML_row_values)
        for j in dcmfile:
            DCM_row_values = j.split(';')
            #print("I am in the DCM File:",DCM_row_values)
            if (len(XML_row_values)==3) and (len(DCM_row_values)==3) and (XML_row_values[1] == DCM_row_values[1]):
                combined_values = ';'.join(DCM_row_values) + ";" + XML_row_values[2] + "\n"
                #print(combined_values)
                ffile.write(combined_values)       
                pop_index = xmlfile.index(i)           
                xmlfile.pop(pop_index)
                #ADTF_Name.remove(i)
                break
    ffile.write("#############Remaining Values of ADTF#############")
    #print("remaining elements inside ADTF_Name:",len(xmlfile))
    remaining_values = '\n'.join(xmlfile)
    ffile.write(remaining_values)
    
############### End --> Filteration of .dcm & .xml ###############


# In[11]:


############### Start --> Appending Heading and Creating "updated DCM file" from file "Filteration of .dcm & .xml" ########

############### Goal 1 : Here we want to use over Heading from dcm File data, which is around 20 Lines      ###############
############### Goal 2 : And put that 20 Lines upwards                                                      ###############
############### Goal 3 : After Heading we want to have our updated dcm value to generate exact dcm file     ###############
############### Goal 4 : Here we want to add that words(Like C_AdaPa_ & _f32) and words(Like "AdaAlgo_Get") ###############

ofile_for_heading = open("ADA_default_mod_C03.dcm", "r+")
#print(ofile_for_heading.readline())

heading = ""
end_count = 0
while end_count < 3:
    line_data = ofile_for_heading.readline()
    heading += line_data
    if line_data.strip() == 'END':
        end_count += 1
heading += "\n"        
#print("heading:\n", heading)


# In[12]:


ofilteration = open("4_Filteration_of_dcm_and_xml.csv","r+")
rfilteration= ofilteration.read() 
sp_filteration=rfilteration.split("\n")
#sp_filteration
#print(sp_Data)


# In[13]:


define_dcm=open("ADA_default_mod_C03.dcm","r+")            
rdcm=define_dcm.read()
dcmfile = rdcm.split('\n')

with open('5_updated_dcm_file_from_dcm.dcm','a') as updated:
    updated.write(heading)

for i in range(0,len(sp_filteration)):
    col_values = sp_filteration[i].split(";")
    if len(col_values) >= 3:
        festwert = col_values[1]
        found_in_dcm = False
        for line in dcmfile:
            #print(f"line: {line}")
            if "FESTWERT " in line:
                original_Festwert= line.split("FESTWERT ")[1]
                #print(f"original_Festwert: {original_Festwert}")
                if festwert in original_Festwert:
                    festwert=original_Festwert
                    found_in_dcm = True
                    break
        if found_in_dcm is False:
            festwert = "AdaAlgo_Get" + festwert
    
        wert = col_values[2]
        Einheit_W = '""'
        main_string = f"FESTWERT {festwert}\n   LANGNAME {festwert}\n   EINHEIT_W {Einheit_W}\n   WERT   {wert}\nEND\n\n"
        with open('5_updated_dcm_file_from_dcm.dcm','a') as updated:
            dcm=updated.write(main_string)
            #print(dcm.count("FESTWERT"))

############### END --> Appending Heading and Creating "updated DCM file" from file "Filteration of .dcm & .xml" ###############

