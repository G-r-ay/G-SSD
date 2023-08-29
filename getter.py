import pandas as pd
import requests
from data_preprocessing import getData,label_dataframe
import streamlit as st
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

@st.cache_data
def get_existing_user_round_data(round_id):
    print('call_exist')
    return pd.read_parquet(f'https://raw.githubusercontent.com/G-r-ay/G-SSD/main/archives/{round_id}.parquet')

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

@st.cache_data
def get_sybil_addresses(round_id):
    print('call_s_l')
    json_content = requests.get(f"https://raw.githubusercontent.com/G-r-ay/G-SSD/main/archives/{round_id}_sybil_cluster.json").json()
    unique_values = list(set(value for values_list in json_content.values() for value in values_list))
    return unique_values

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

@st.cache_data
def get_existing_time_data(round_id):
    print('call_exist_time')
    return pd.read_parquet(f'https://raw.githubusercontent.com/G-r-ay/G-SSD/main/archives/{round_id}_time.parquet')

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

@st.cache_data
def get_date_existing(round_id,sybil_addresses):
    raw = getData(round_id,True)
    existing_data = get_existing_time_data(round_id)
    print('data')
    time_data = pd.merge(raw,existing_data,on='transaction')
    time_data = label_dataframe(time_data,sybil_addresses)
    return time_data

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

@st.cache_data
def get_labelled_existing(round_id):
    raw = getData(round_id,True)
    print('data')
    sybil_addresses = get_sybil_addresses(round_id)
    print('data')
    labelled_data = label_dataframe(raw, sybil_addresses)
    print('data')
    return labelled_data,sybil_addresses

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
