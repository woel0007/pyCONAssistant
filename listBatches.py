import requests
import json
import credManager

iconURL = 'https://secure3.iconcmo.com/api/'
authDetails = credManager.getCredentials('user.conf')

authString = '{' \
                 '"Auth": {' \
                     '"Phone":",' + authDetails[0] + '",' \
                     '"Username":"' + authDetails[1] + '",' \
                     '"Password":"' + authDetails[2] + '"' \
                 '},' \
                 '"Request": {' \
                     '"Module":"GL",' \
                     '"Section":"Accounts"' \
                 '}' \
             '}'

authStringBytes = str.encode(authString)

r = requests.post(iconURL, json=authString, verify=False)

print(r.text)
