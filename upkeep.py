import pandas as pd
import json
import streamlit as st
from data_preprocessing import preprocess_data,merger,getData,label_dataframe
from user_data_fuctions import compile_data
from similarity_code import address_similarity
#---------------------------------------------------------------------------------------------------------------

def performUpKeep(updates,processed_data,round_id):
    compile_data(updates,round_id)
    existing_data = pd.read_csv(f'https://raw.githubusercontent.com/G-r-ay/G-SSD/main/archives/{round_id}.csv')
    fit_data = merger(existing_data,processed_data)
    s_address = address_similarity(fit_data)
    return s_address
#---------------------------------------------------------------------------------------------------------------

def checkUpKeep(round_id):
    raw = getData(round_id)
    processed_data = preprocess_data(raw)  
    existing_data = pd.read_csv(f'https://raw.githubusercontent.com/G-r-ay/G-SSD/main/archives/{round_id}.csv')
    updates = list(set(processed_data['voter'].unique()) - set(existing_data['voter'].unique()))[5000:13000]
    addresses = list(filter(lambda item: item not in existing_data,updates))
    print(len(addresses))
    print(len(updates))
    if len(addresses) > 5:
        sybil_addresses = performUpKeep(updates,processed_data,round_id)
        labelled_data = label_dataframe(raw,sybil_addresses)
        return labelled_data
    else:
        print('upkeepnotneeded')
        fit_data = merger(existing_data,processed_data)
        sybil_addresses = address_similarity(fit_data)
        labelled_data = label_dataframe(raw,sybil_addresses)
        print('tested_updates')
        return labelled_data
#---------------------------------------------------------------------------------------------------------------









