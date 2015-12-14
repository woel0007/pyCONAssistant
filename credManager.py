import re

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