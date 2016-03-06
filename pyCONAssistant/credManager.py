import re
import requests
import json
import sys
from pyCONAssistant import globals

def getCredentials(credfile):

    fhcontents = ""
    try:
        fh = open(credfile)
        fhcontents = fh.read()
        fh.close()
    except:
        print("Error reading credential file.")

    if(len(fhcontents) > 0):
        iconPhone = re.findall(r"phone=(.+)", fhcontents)[0]
        iconUser = re.findall(r"user=(.+)", fhcontents)[0]
        iconPass = re.findall(r"pass=(.+)", fhcontents)[0]
        return [iconPhone, iconUser, iconPass]
    else:
        return ['unknown', 'unknown', 'unknown']


def requestSessionID():

    authTokenList = getCredentials('C:\\Users\\opjxw0\\Documents\\sourceCode\\pyCONAssistant\\user.conf')
    headers = headers = {'content-type': 'application/json'}
    jsonAuthString = '{"Auth": {"Phone":"' + authTokenList[0] + '","Username":"' + authTokenList[1] + '","Password":"' + authTokenList[2] + '"},"Request": {"Module":"GL","Section":"Accounts"}}'

    r = requests.post(globals.iconAPIURL, jsonAuthString, headers=headers)
    data = json.loads(r.text)
    return data["session"]

