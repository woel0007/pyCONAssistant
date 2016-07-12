import requests
import json
from globals import batchRangeStartDate, batchRangeEndDate, FundsNotRecordedAtBank, credFile, iconAPIURL, GFList
from credManager import getCredentials, requestSessionID
import sys

def getRawContributionData(sessID):

    startIndex = 1
    limit = 100
    totalRecords = 2
    partBatchList = []

    while(startIndex < totalRecords):
        headers = headers = {'content-type': 'application/json'}
        jsonString = '{"Auth": { "Session" : "' + sessID + '"},"Request": {"Module": "contributions", "Section": "posted", "Filters": {"begin_date": "' + batchRangeStartDate + '", "end_date": "' + batchRangeEndDate + '", "startAt": "' + str(startIndex) + '", "limit": "' + str(limit) + '" }}}'
        r = requests.post(iconAPIURL, jsonString, headers=headers)
        data = json.loads(r.text)
        partBatchList = partBatchList + data['posted']

        totalRecords = data['statistics']['records']
        startIndex = startIndex + limit

    return partBatchList


def displayGFContributionsByMonth(sessID):

    batches = getRawContributionData(sessID)
    monthBatchDict = {}

    for cont in batches:
        if cont['fund_name'] in GFList:
            month = cont['date_given'][5:7]
            if month in monthBatchDict:
                monthBatchDict[month] += float(cont['amount'][1:])
            else:
                monthBatchDict[month] = float(cont['amount'][1:])

    for mon in monthBatchDict:
        monthBatchDict[mon] = int(round(monthBatchDict[mon]))

    for mon in sorted(monthBatchDict):
        print(mon + '\t' + str(monthBatchDict[mon]))


def displayGFContributionsByBatch(sessID):

    batches = getRawContributionData(sessID)
    batchDict = {}

    for cont in batches:
        if(cont['fund_name'] not in FundsNotRecordedAtBank):
            if(cont['date_given'] in batchDict):
                batchDict[cont['date_given']] += float(cont['amount'][1:])
            else:
                batchDict[cont['date_given']] = float(cont['amount'][1:])

    for batch in sorted(batchDict):
        print(batch + '\t' + str(batchDict[batch]))



if __name__ == "__main__":

    # Login
    if sys.argv.__len__() > 1:
        credFile = sys.argv[1]

    authTokenList = getCredentials(credFile)
    sessID = requestSessionID(authTokenList)

    # Execute function to output results
    displayGFContributionsByBatch(sessID)


    displayGFContributionsByBatch()

