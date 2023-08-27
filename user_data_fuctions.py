import requests
import pandas as pd
import datetime 
import streamlit as st
from update_db import update_repo_data,update_round_time_data
import requests
from requests.auth import HTTPBasicAuth
import time
import http.client
from requests.exceptions import ConnectionError, Timeout, JSONDecodeError
#---------------------------------------------------------------------------------------------------------------
colavent_api_key = st.secrets['colavent_api_key']

api_key= st.secrets["api_key"]
#---------------------------------------------------------------------------------------------------------------
url = "https://api-optimistic.etherscan.io/api"

#---------------------------------------------------------------------------------------------------------------

def first_last_info(address):

    params = {
        "module": "account",
        "action": "txlist",
        "address": address,
        "page": 1,
        "offset": 100,
        "startblock": 0,
        "endblock": 99999999,
        "sort": "asc",
        "apikey": api_key
    }

    response = requests.get(url, params=params).json()
    response = response['result']
    first_date = response[0]['timeStamp']
    last_date = response[-1]['timeStamp']

    first_to = response[0]['to']
    first_from = response[0]['from']

    last_to = response[-1]['to']
    last_from = response[-1]['from']

    if first_to == address:
        first_to = 'self'
    if first_from == address:
        first_from = 'self'
    if last_to == address:
        last_to = 'self'
    if last_from == address:
        last_from = 'self'

    return [first_date, last_date, first_from, first_to, last_from, last_to]
#---------------------------------------------------------------------------------------------------------------

def get_transaction_history(address):

        params = {
            "module": "account",
            "action": "txlist",
            "address": address,
            "page": 1,
            "offset": 100,
            "startblock": 0,
            "endblock": 99999999,
            "sort": "asc",
            "apikey": api_key
        }

        response = requests.get(url, params=params).json()
        return response['result']


# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


def get_Erc20_transaction_history(address):

    params = {
        "module": "account",
        "action": "tokentx",
        "address": address,
        "page": 1,
        "offset": 100,
        "startblock": 0,
        "endblock": 99999999,
        "sort": "asc",
        "apikey": api_key
    }

    response = requests.get(url, params=params).json()
    return response['result']
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def get_suppler_contract(address):

    params = {
        "module": "account",
        "action": "txlistinternal",
        "address": address,
        "page": 1,
        "offset": 100,
        "startblock": 0,
        "endblock": 99999999,
        "sort": "asc",
        "apikey": api_key
    }

    response = requests.get(url, params=params).json()
    return response['result'][-1]
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


def get_wallet_age(history: list[dict]):
    if len(history) > 0:
        creation_time = int(history[0]['timeStamp']) #type:ignore
        creation_date = datetime.datetime.fromtimestamp(creation_time).date()
        current_date = datetime.date.today()
        wallet_age = (current_date - creation_date).days
        return wallet_age
    else:
        return 0
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


def to_and_from(history: list[dict], address):
    from_count = 0
    to_count = 0
    for transactions in history:
        if transactions['from'] == address:
            from_count += 1
        else:
            to_count += 1
    return from_count, to_count
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


def fetch(address, nested_list):

    reg_hist = get_transaction_history(address)
    trasacting_hist = first_last_info(address)
    erc20_hist = get_Erc20_transaction_history(address)

    txn_count = len(reg_hist)

    reg_age = get_wallet_age(reg_hist)
    erc_age = get_wallet_age(erc20_hist)

    reg_to, reg_from = to_and_from(reg_hist, address)
    erc_to, erc_from = to_and_from(erc20_hist, address)

    row = [address, txn_count, reg_age, erc_age, reg_to,reg_from, erc_to, erc_from] + trasacting_hist
    nested_list.append(row)

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def compile_data(addresses,round_id):

    headers = ['voter','txn_count','Wallet_Age','Wallet_Age(Erc20)','to_count','from_count','erc_to','erc_from','first_date','last_date','first_from','first_to','last_from','last_to']
    contents = []
    count = 0
    my_bar = st.progress(0)
    total_items = len(addresses)
    for count, address in enumerate(addresses, start=1):
        try:
            fetch(address, contents)
            time.sleep(1)
            progress_text = f"Updating Round data. Please wait.: {count}/{total_items}"
            my_bar.progress(int(count * 100 / total_items),progress_text)
        except (ConnectionError, Timeout,http.client.RemoteDisconnected,TypeError,JSONDecodeError) as e:
            print(f'Failed to fetch data for {address}: Error Type{e}')
            break
    my_bar.empty()
    print('saving')
    new_data_df = pd.DataFrame(contents, columns=headers)
    update_repo_data(round_id, new_data_df)



def get_dates(hashes, round_id):
    contents = []
    count = 0
    my_bar = st.progress(0)
    total_items = len(hashes)
    for count, tx_hash in enumerate(hashes, start=1):
        try:
            url = f"https://api.covalenthq.com/v1/optimism-mainnet/transaction_v2/{tx_hash}/?"

            headers = {
                "accept": "application/json",
            }

            basic = HTTPBasicAuth(colavent_api_key, '')

            response = requests.get(url, headers=headers, auth=basic).json()['data']['items'][0]['block_signed_at']
            contents.append([tx_hash, response])
            progress_text = f"Updating Round date data. Please wait.: {count}/{total_items}"
            my_bar.progress(int(count * 100 / total_items),progress_text)
        except (ConnectionError, Timeout, http.client.RemoteDisconnected, TypeError, JSONDecodeError) as e:
            print(f'Failed to fetch data for {tx_hash}: Error Type {e}')
            break
    my_bar.empty()
    print('saving dates')
    headers = ['transaction', 'date']
    new_dates = pd.DataFrame(contents, columns=headers)
    update_round_time_data(round_id, new_dates)
