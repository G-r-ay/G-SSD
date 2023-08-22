import pandas as pd
import json
import streamlit as st
from data_preprocessing import preprocess_data,merger,getData,label_dataframe
from user_data_fuctions import compile_data
from similarity_code import address_similarity

def performUpKeep(updates,existing_data,processed_data,round_id):
    compile_data(updates,existing_data,round_id)
    existing_data = pd.read_csv(f'archives/{round_id}.csv')
    fit_data = merger(existing_data,processed_data)
    s_address = address_similarity(fit_data)
    return s_address


@st.cache_data
def checkUpKeep(round_id,data_mode):
    raw = getData(round_id)
    processed_data = preprocess_data(raw)
    if data_mode == "Server":
        existing_data = pd.read_csv(f'archives/{round_id}.csv')
        updates = list(set(processed_data['voter']) - set(existing_data['voter']))

        addresses = list(filter(lambda item: item not in existing_data,updates))
        if len(addresses) > 5:
            sybil_addresses = performUpKeep(updates,existing_data,processed_data,round_id)
            labelled_data = label_dataframe(raw,sybil_addresses)
            return labelled_data
        else:
            print('upkeepnotneeded')
            with open("archives/sybil_clusters.json", "r") as json_file:
                data = json.load(json_file)
            sybil_addresses = list(set(value for sublist in data.values() for value in sublist))
            labelled_data = label_dataframe(raw,sybil_addresses)
            return labelled_data
    else:
        existing_data = pd.read_csv(f'https://raw.githubusercontent.com/G-r-ay/G-SSD/main/archives/{round_id}.csv')
        fit_data = merger(existing_data,processed_data)
        address = address_similarity(fit_data)
        labelled_data = label_dataframe(raw,address)
        return labelled_data









