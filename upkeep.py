import pandas as pd
import streamlit as st
from data_preprocessing import preprocess_data,merger,getData,label_dataframe
from user_data_fuctions import compile_data,get_dates
from similarity_code import address_similarity
#---------------------------------------------------------------------------------------------------------------

def performUpKeep(updates,processed_data,round_id):
    compile_data(updates,round_id)
    existing_data = pd.read_parquet(f'https://raw.githubusercontent.com/G-r-ay/G-SSD/main/archives/{round_id}.parquet')
    fit_data = merger(existing_data,processed_data)
    s_address = address_similarity(fit_data,round_id)
    return s_address
#---------------------------------------------------------------------------------------------------------------
def checkUpKeep(round_id):
    raw = getData(round_id)
    processed_data = preprocess_data(raw)
    existing_data = pd.read_parquet(f'https://raw.githubusercontent.com/G-r-ay/G-SSD/main/archives/{round_id}.parquet')
    updates = list(set(processed_data['voter'].unique()) - set(existing_data['voter'].unique()))
    addresses = list(filter(lambda item: item not in existing_data,updates))
    if len(addresses) > 5:
        sybil_addresses = performUpKeep(updates,processed_data,round_id)
        labelled_data = label_dataframe(raw,sybil_addresses)
        return labelled_data,sybil_addresses
    else:
        print('upkeepnotneeded')
        fit_data = merger(existing_data,processed_data)
        sybil_addresses = address_similarity(fit_data,round_id)
        labelled_data = label_dataframe(raw,sybil_addresses)
        return labelled_data
#---------------------------------------------------------------------------------------------------------------
def date_up_keep(round_id,sybil_addresses):
    raw = getData(round_id,True)
    existing_data = pd.read_parquet(f'https://raw.githubusercontent.com/G-r-ay/G-SSD/main/archives/{round_id}_time.parquet')
    updates = list(set(raw['transaction'].unique())-set(existing_data['transaction'].unique()))
    get_dates(updates,round_id)
    existing_data = pd.read_parquet(f'https://raw.githubusercontent.com/G-r-ay/G-SSD/main/archives/{round_id}_time.parquet')
    print('done')
    time_data = pd.merge(raw,existing_data,on='transaction')
    time_data = label_dataframe(time_data,sybil_addresses)
    return time_data






