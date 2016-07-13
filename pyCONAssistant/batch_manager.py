"""
Fill in description

:param sess_id:
:return:
"""

import json
import sys

import requests

from pyCONAssistant.globals import BATCH_RANGE_START_DATE, BATCH_RANGE_END_DATE, \
                                   FUNDS_NOT_RECORDED_AT_BANK, DEFAULT_CRED_FILE, \
                                   ICON_API_URL, GENERAL_FUND_LIST
from pyCONAssistant.cred_manager import get_credentials, request_session_id


def get_raw_contribution_data(sess_id):
    """
    Fill in description

    :param sess_id:
    :return:
    """

    start_index = 1
    limit = 100
    total_records = 2
    partial_batch_list = []

    while start_index < total_records:
        headers = {'content-type': 'application/json'}
        json_string = '{"Auth": { "Session" : "' + sess_id + '"},' \
                       '"Request": {"Module": "contributions", "Section": "posted", ' \
                       '"Filters": {"begin_date": "' + BATCH_RANGE_START_DATE + '", ' \
                                   '"end_date": "' + BATCH_RANGE_END_DATE + '", ' \
                                   '"startAt": "' + str(start_index) + '", ' \
                                   '"limit": "' + str(limit) + '" }}}'
        resp = requests.post(ICON_API_URL, json_string, headers=headers)
        data = json.loads(resp.text)
        partial_batch_list = partial_batch_list + data['posted']

        total_records = data['statistics']['records']
        start_index = start_index + limit

    return partial_batch_list


def display_gf_conts_by_month(session_id):
    """
    Fill in description

    :param sess_id:
    :return:
    """

    batches = get_raw_contribution_data(session_id)
    month_batch_dict = {}

    for cont in batches:
        if cont['fund_name'] in GENERAL_FUND_LIST:
            month = cont['date_given'][5:7]
            if month in month_batch_dict:
                month_batch_dict[month] += float(cont['amount'][1:])
            else:
                month_batch_dict[month] = float(cont['amount'][1:])

    for mon in month_batch_dict:
        month_batch_dict[mon] = int(round(month_batch_dict[mon]))

    for mon in sorted(month_batch_dict):
        print mon + '\t' + str(month_batch_dict[mon])


def display_gf_conts_by_batch(session_id):
    """
    Fill in description

    :param sess_id:
    :return:
    """

    batches = get_raw_contribution_data(session_id)
    batch_dict = {}

    for cont in batches:
        if cont['fund_name'] not in FUNDS_NOT_RECORDED_AT_BANK:
            if cont['date_given'] in batch_dict:
                batch_dict[cont['date_given']] += float(cont['amount'][1:])
            else:
                batch_dict[cont['date_given']] = float(cont['amount'][1:])

    for batch in sorted(batch_dict):
        print batch + '\t' + str(batch_dict[batch])



if __name__ == "__main__":

    # Login - determine if cred_file is being passed from command-line invocation or
    #   whether to use default.
    CRED_FILE = ''
    if sys.argv.__len__() > 1:
        CRED_FILE = sys.argv[1]
    else:
        CRED_FILE = DEFAULT_CRED_FILE
    AUTH_TOKEN_LIST = get_credentials(CRED_FILE)

    # Execute function to output results
    display_gf_conts_by_batch(request_session_id(AUTH_TOKEN_LIST))
