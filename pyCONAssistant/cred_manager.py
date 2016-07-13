"""
Fill in module docstring


"""
import re
import json

import requests

from pyCONAssistant.globals import ICON_API_URL

def get_credentials(credfile):
    """
    Fill in details.

    :param credfile:
    :return:
    """

    fhcontents = ""
    try:
        file_handle = open(credfile)
        fhcontents = file_handle.read()
    except IOError:
        print "Error reading credential file."
    finally:
        file_handle.close()

    if len(fhcontents) > 0:
        icon_phone = re.findall(r"phone=(.+)", fhcontents)[0]
        icon_user = re.findall(r"user=(.+)", fhcontents)[0]
        icon_pass = re.findall(r"pass=(.+)", fhcontents)[0]
        return [icon_phone, icon_user, icon_pass]
    else:
        return ['unknown', 'unknown', 'unknown']


def request_session_id(auth_token_list):
    """
    Fill in details.

    :param credfile:
    :return:
    """

    headers = {'content-type': 'application/json'}
    json_auth_string = '{"Auth": {"Phone":"' + auth_token_list[0] + '",' \
                        '"Username":"' + auth_token_list[1] + '",' \
                        '"Password":"' + auth_token_list[2] + '"},' \
                        '"Request": {"Module":"GL","Section":"Accounts"}}'

    # Validate JSON string to ensure it's properly encoded.
    try:
        json.loads(json_auth_string)
    except ValueError:
        pass

    resp = requests.post(ICON_API_URL, json_auth_string, headers=headers)
    if resp.status_code == 200:
        data = json.loads(resp.text)
    else:
        pass
    return data["session"]
