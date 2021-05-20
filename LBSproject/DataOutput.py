#!/usr/bin/env python
# coding: utf-8

# ### DATA OUTPUT
# **Data output request and converting response to .csv file**

# In[1]:


import requests
from requests.auth import HTTPBasicAuth
import json
import xmltodict
import csv
import time

##### DEFINE A RECURSIVE FUNCTION TO EXTRACT ALL FIELDS FROM THE RESPONSE #####
toHeader = []
toWrite = []
def RecursiveWriting(dictionary):
    if isinstance(dictionary, list):
        for j in range (len(dictionary)):
            return RecursiveWriting(dictionary[j])
    elif isinstance(dictionary, dict):
        key = list(dictionary.keys())
        value = list(dictionary.values())
    
    for i in range (len(dictionary)):
        if isinstance(value[i], dict):
            RecursiveWriting(value[i])
        elif isinstance(value[i],list):
            RecursiveWriting(value[i])
        else:
            toHeader.append(key[i])
            toWrite.append(value[i])
    return toHeader,toWrite



#### READING JSON CONFIG ####
with open('apiConfig.json') as file:
    dictC = json.load(file)

    
#### OPEN WEB SESSION TO KEEP IN MEMORY ALL COOKIES AND THEN API CALL ####
session = requests.session()
getLoginCookie_API = session.get(dictC['BaseURL']+dictC['login'], 
                                 auth = HTTPBasicAuth(dictC['username'],dictC['pw']), 
                                 headers = dictC['headers'])
getDataOutput_API = session.get(dictC['BaseURL']+dictC['dataOutput'], 
                                         params = dictC['paramDataOutput'], 
                                         headers = dictC['headers'])



# for this dictionary, it is necessary to use manipulation string #
# 'cause of the dict parsing fault casued by the first line of the response: #
# (<?xml version [...]>) #
dataOutput_API_start = ((getDataOutput_API.content).decode('utf-8')).find('>')+1
dataOutput_API_string = (getDataOutput_API.content).decode('utf-8')[dataOutput_API_start:]
dictDataOutput_API = xmltodict.parse(dataOutput_API_string.encode('utf-8'))



#### EXTRACT DATA & WRITE .CSV ####
chiave,valore = RecursiveWriting(dictDataOutput_API)
with open('dataOutput_'+time.strftime("%Y%m%d-%H%M%S")+'.csv', 'w', newline='') as csv_file:
    csvwriter = csv.writer(csv_file, delimiter = '|')
    csvwriter.writerow(chiave) 
    csvwriter.writerow(valore)


# In[ ]:




