import pandas as pd
from getter import *
from data_preprocessing import preprocess_data,merger,getData,label_dataframe
from user_data_fuctions import compile_data,get_dates
from similarity_code import address_similarity

#---------------------------------------------------------------------------------------------------------------
def performUpKeep(updates,processed_data,round_id,existing_data):
    print('starting')
    compile_data(updates,round_id,existing_data)
    fit_data = merger(existing_data,processed_data)
    s_address = address_similarity(fit_data,round_id)
    return s_address
#---------------------------------------------------------------------------------------------------------------
def checkUpKeep(round_id):
    print('starter')
    raw = getData(round_id)
    print('data')
    processed_data = preprocess_data(raw)
    print('data')
    existing_data = get_existing_user_round_data(round_id)
    updates = list(set(processed_data['voter'].unique()) - set(existing_data['voter'].unique()))
    if len(updates) > 5:
        print('data1')
        sybil_addresses = performUpKeep(updates,processed_data,round_id,existing_data)
        labelled_data = label_dataframe(raw,sybil_addresses)
        return labelled_data,sybil_addresses
    else:
        print('upkeepnotneeded')
        sybil_addresses = get_sybil_addresses(round_id)
        labelled_data = label_dataframe(raw,sybil_addresses)
        return labelled_data,sybil_addresses
#---------------------------------------------------------------------------------------------------------------



    
def date_up_keep_update(round_id,sybil_addresses):
    raw = getData(round_id,True)
    existing_data = get_existing_time_data(round_id)
    print('starting')
    updates = list(set(raw['transaction'].unique())-set(existing_data['transaction'].unique()))
    get_dates(updates,round_id)
    existing_data = pd.read_parquet(f'https://raw.githubusercontent.com/G-r-ay/G-SSD/main/archives/{round_id}_time.parquet')
    time_data = pd.merge(raw,existing_data,on='transaction')
    time_data = label_dataframe(time_data,sybil_addresses)
    return time_data






