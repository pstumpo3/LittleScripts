#!/usr/bin/env python
# coding: utf-8

# ### GetUniverse
# **GetUniverse request and converting response to .csv file**

# In[1]:


import requests
from requests.auth import HTTPBasicAuth
import json
import xmltodict
import csv
import time


#### READING JSON CONFIG ####
with open('apiConfig.json') as file:
    dictC = json.load(file)


#### OPEN WEB SESSION TO KEEP IN MEMORY ALL COOKIES AND THEN API CALL ####
session = requests.session()
getLoginCookie_API = session.get(dictC['BaseURL']+dictC['login'], 
                                 auth = HTTPBasicAuth(dictC['username'],dictC['pw']), 
                                 headers = dictC['headers'])
getUniverse_API = session.get(dictC['BaseURL']+dictC['getUniverse'], 
                                         params = dictC['paramGetUniverse'], 
                                         headers = dictC['headers'])

#### EXTRACT DATA & WRITE .CSV ####

dictGetUniverse_API = xmltodict.parse(getUniverse_API.content)

columnName = list(dictC['responseColumnUniverse'].values())
keyLNT = dictC['keyLastUpdated_NT']


with open('getUniverse_'+time.strftime("%Y-%m-%d_%H-%M-%S")+'.csv', 'w', newline = '') as csv_file:
    csvwriter = csv.writer(csv_file, delimiter = '|')
    csvwriter.writerow(columnName)
    for fundShareClassList in dictGetUniverse_API:
        for shareClass in (dictGetUniverse_API[fundShareClassList]):
            for i in range (len(dictGetUniverse_API[fundShareClassList][shareClass])):
                for j in range (len(dictGetUniverse_API[fundShareClassList][shareClass][i][keyLNT])):
                    
                    ###### only with @_Type = 4, the response contains @_Id values ######
                    if (dictGetUniverse_API[fundShareClassList][shareClass][i][keyLNT][j][columnName[7]] == '4'):
                        csvwriter.writerow([shareClass, 
                                            dictGetUniverse_API[fundShareClassList][shareClass][i][columnName[1]],
                                            dictGetUniverse_API[fundShareClassList][shareClass][i][columnName[2]],
                                            dictGetUniverse_API[fundShareClassList][shareClass][i][columnName[3]],
                                            dictGetUniverse_API[fundShareClassList][shareClass][i][columnName[4]],
                                            dictGetUniverse_API[fundShareClassList][shareClass][i][columnName[5]], 
                                            dictGetUniverse_API[fundShareClassList][shareClass][i][columnName[6]],
                                            dictGetUniverse_API[fundShareClassList][shareClass][i][keyLNT][j][columnName[7]],
                                            dictGetUniverse_API[fundShareClassList][shareClass][i][keyLNT][j][columnName[8]],
                                            dictGetUniverse_API[fundShareClassList][shareClass][i][keyLNT][j][columnName[9]]])
                    else:
                        csvwriter.writerow([shareClass, 
                                            dictGetUniverse_API[fundShareClassList][shareClass][i][columnName[1]],
                                            dictGetUniverse_API[fundShareClassList][shareClass][i][columnName[2]],
                                            dictGetUniverse_API[fundShareClassList][shareClass][i][columnName[3]],
                                            dictGetUniverse_API[fundShareClassList][shareClass][i][columnName[4]],
                                            dictGetUniverse_API[fundShareClassList][shareClass][i][columnName[5]], 
                                            dictGetUniverse_API[fundShareClassList][shareClass][i][columnName[6]],
                                            dictGetUniverse_API[fundShareClassList][shareClass][i][keyLNT][j][columnName[7]],
                                            'N/A', #Not Available
                                            dictGetUniverse_API[fundShareClassList][shareClass][i][keyLNT][j][columnName[9]]])


# In[ ]:




