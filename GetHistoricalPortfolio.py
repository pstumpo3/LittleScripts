#!/usr/bin/env python
# coding: utf-8

# ### GetHistoricalPortfolio
# **GetHistoricalPortfolio request and converting response to .csv file**

# In[23]:


import requests
from requests.auth import HTTPBasicAuth
import json
from xml.etree import ElementTree
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
getHistoricalPortfolio_API = session.get(dictC['BaseURL']+dictC['getPortfolio'], 
                                         params = dictC['paramGetHistoricalPortfolio'], 
                                         headers = dictC['headers'])


#### EXTRACT DATA & WRITE CSV ####
dictGetHistoricalPortfolio_API = xmltodict.parse(getHistoricalPortfolio_API.content)

columnName = list(dictC['responseColumnPortfolio'].values())

with open('getHistoricalPortfolio_'+time.strftime("%Y-%m-%d_%H-%M-%S")+'.csv', 'w', newline = '') as csv_file:
    csvwriter = csv.writer(csv_file, delimiter = '|')
    csvwriter.writerow(columnName)
    for portfolioList in dictGetHistoricalPortfolio_API:
        for portfolio in (dictGetHistoricalPortfolio_API[portfolioList]):
            for i in range (len(dictGetHistoricalPortfolio_API[portfolioList][portfolio])):
                
                csvwriter.writerow([portfolio, 
                                    dictGetHistoricalPortfolio_API[portfolioList][portfolio][i][columnName[1]],
                                    dictGetHistoricalPortfolio_API[portfolioList][portfolio][i][columnName[2]],
                                    dictGetHistoricalPortfolio_API[portfolioList][portfolio][i][columnName[3]],
                                    dictGetHistoricalPortfolio_API[portfolioList][portfolio][i][columnName[4]]])

