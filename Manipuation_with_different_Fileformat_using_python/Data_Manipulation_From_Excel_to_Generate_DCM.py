#!/usr/bin/env python
# coding: utf-8

# In[1]:


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


# In[2]:


ofilteration = open("4_Filteration_of_dcm_and_xml.csv","r+")
rfilteration= ofilteration.read() 
sp_filteration=rfilteration.split("\n")
#sp_filteration
#print(sp_Data)


# In[3]:


define_dcm=open("ADA_default_mod_C03.dcm","r+")            
rdcm=define_dcm.read()
dcmfile = rdcm.split('\n')

with open('6_updated_dcm_file_from_excel.dcm','a') as updated:
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
        with open('6_updated_dcm_file_from_excel.dcm','a') as updated:
            dcm=updated.write(main_string)
            #print(dcm.count("FESTWERT"))

############### END --> Appending Heading and Creating "updated DCM file" from file "Filteration of .dcm & .xml" ##########

