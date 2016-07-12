import re
import requests
import json
import sys
from globals import *

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


def requestSessionID(auth_token_list):

    headers = headers = {'content-type': 'application/json'}
    jsonAuthString = '{"Auth": {"Phone":"' + auth_token_list[0] + '","Username":"' + auth_token_list[1] + '","Password":"' + auth_token_list[2] + '"},"Request": {"Module":"GL","Section":"Accounts"}}'


    r = requests.post(iconAPIURL, jsonAuthString, headers=headers)
    if r.status_code == 200:
        data = json.loads(r.text)
    else:
        pass
    return data["session"]

