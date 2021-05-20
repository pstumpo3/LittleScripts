import time
from itertools import chain
import email
import imaplib
from email.header import decode_header
import webbrowser
import os

## This script REQUIRES "requests": http://docs.python-requests.org/
## TO INSTALL: pip install requests
import requests
import json

with open('Config.json') as f:
    dictC = json.load(f)

# This method runs a POST call to Refresh Token and a second API call to add a new item in a Queue stored in UiPath Orchestrator(Cloud). 
# It receives as input arguments the email sender and subject
def apiOrchestrator(arg1, arg2):
        
       
    try:
        # N.B -> For Orchestrator On-premises please see UiPath API Swagger  
        r = requests.post(url=dictC['URL_Auth'], json= dictC['bodyAuth'], headers=dictC['headersAuth'] )
        response = json.loads(r.content)
        print( "Bearer "+response["access_token"])
        headers2 = dictC['headersAddQI']
        headers2['Authorization'] = "Bearer "+response["access_token"]

        # API call set-up for add new queue-item
        specificContent = {}
        specificContent['email'] = arg1
        specificContent['email@odata.type'] = '#String'
        specificContent['Email-Subject'] = arg2
        specificContent['Email-Subject@odata.type'] = '#String'
        data2 ={}
        data2['Name'] = dictC['queueName']
        data2['Priority'] = dictC['queuePriority']
        data2['SpecificContent'] = specificContent
        data3 = {}
        data3['itemData'] = data2
        r2 = requests.post(url=dictC['URL_AddQI'], data = json.dumps(data3), headers = headers2)
        print(r2.content)
        
    except Exception as exception:
        print("Exception: {}".format(type(exception)))
        print("Exception message: {}".format(exception))

iteration=1

# Email Listener
while 1:

    try:
        print("{}{}".format("Iteration number: ",iteration))
        iteration=iteration+1

        # Connection
        imap = imaplib.IMAP4_SSL(dictC['EmailCredentials']['imap_Host'] , dictC['EmailCredentials']['imap_Port'])

        # Log-in
        imap.login(dictC['EmailCredentials']['username'],dictC['EmailCredentials']['password'] )

        # Folder to listen
        status, messages = imap.select(dictC['EmailSelection']['folderName'])

        # Filter not case-sensitive
        subject=dictC['EmailSelection']['filter']
        result, data = imap.search(None,'(UNSEEN SUBJECT "%s")' % subject)
        
        for num in data[0].split():
            typ, data = imap.fetch(num, '(RFC822)')
            for response in data:
                if isinstance(response, tuple):
                    msg = email.message_from_string(response[1].decode('utf-8'))
                    print(msg["Date"])
                    print(msg["From"])
                    print(msg["Subject"])
                    start = str(msg['From']).find('<') + 1
                    end = str(msg['From']).find('>', start)
                    emailSender = (str(msg['From'][start:end]))

                    # apiOrchestrator() is called to add a new item into a Queue
                    apiOrchestrator(emailSender, str(msg["Subject"]))

        # Close the connection and log-out
        imap.close()
        imap.logout()
        
        # Set-up the sleeping time for optimal trade-off
        time.sleep(1)
        
    except Exception as exception:
        print("Exception: {}".format(type(exception)))
        print("Exception message: {}".format(exception))

