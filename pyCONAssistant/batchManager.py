import requests
import json
from pyCONAssistant import globals
from pyCONAssistant import credManager


def getRawContributionData():

    startIndex = 1
    limit = 100
    totalRecords = 2
    partBatchList = []

    while(startIndex < totalRecords):
        headers = headers = {'content-type': 'application/json'}
        jsonString = '{"Auth": { "Session" : "' + credManager.requestSessionID() + '"},"Request": {"Module": "contributions", "Section": "posted", "Filters": {"begin_date": "' + globals.batchRangeStartDate + '", "end_date": "' + globals.batchRangeEndDate + '", "startAt": "' + str(startIndex) + '", "limit": "' + str(limit) + '" }}}'
        r = requests.post(globals.iconAPIURL, jsonString, headers=headers)
        data = json.loads(r.text)
        partBatchList = partBatchList + data['posted']

        totalRecords = data['statistics']['records']
        startIndex = startIndex + limit

    return partBatchList


def displayGFContributionsByMonth():

    batches = getRawContributionData()
    monthBatchDict = {}

    for cont in batches:
        if cont['fund_name'] in globals.GFList:
            month = cont['date_given'][5:7]
            if month in monthBatchDict:
                monthBatchDict[month] += float(cont['amount'][1:])
            else:
                monthBatchDict[month] = float(cont['amount'][1:])

    for mon in monthBatchDict:
        monthBatchDict[mon] = int(round(monthBatchDict[mon]))

    for mon in sorted(monthBatchDict):
        print(mon + '\t' + str(monthBatchDict[mon]))


def displayGFContributionsByBatch():

    batches = getRawContributionData()
    batchDict = {}

    for cont in batches:
        if(cont['fund_name'] not in globals.FundsNotRecordedAtBank):
            if(cont['date_given'] in batchDict):
                batchDict[cont['date_given']] += float(cont['amount'][1:])
            else:
                batchDict[cont['date_given']] = float(cont['amount'][1:])

    for batch in sorted(batchDict):
        print(batch + '\t' + str(batchDict[batch]))

