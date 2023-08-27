import requests
import base64
import streamlit as st
import json
import pandas as pd


#---------------------------------------------------------------------------------------------------------------
github_token= st.secrets["github_token"]
#---------------------------------------------------------------------------------------------------------------
def update_repo_data(round_id,new_data):
    existing_file_url = f'https://raw.githubusercontent.com/G-r-ay/G-SSD/main/archives/{round_id}.parquet'
    data = pd.read_parquet(existing_file_url)
    data.dropna(inplace=True)
    new_data['first_date'] = new_data['first_date'].astype('int64')
    new_data['last_date'] = new_data['last_date'].astype('int64')
    df = pd.concat([data, new_data], ignore_index=True)


    df.drop_duplicates(inplace=True)
    modified_content = df.to_parquet(index=False)
    modified_content_encoded = base64.b64encode(modified_content).decode()

    api_url = f'https://api.github.com/repos/G-r-ay/G-SSD/contents/archives/{round_id}.parquet'

    headers = {
        "Authorization": f"Bearer {github_token}"
    }

    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        file_info = response.json()
        payload = {
            "message": "Update Parquet file",
            "content": modified_content_encoded,
            "sha": file_info["sha"]
        }

        update_response = requests.put(api_url, json=payload, headers=headers)
        if update_response.status_code == 200:
            print("user data updated successfully.")
        else:
            print("Error updating file:", update_response.text)
    else:
        print("Error getting file info:", response.text)
#---------------------------------------------------------------------------------------------------------------
def overwrite_github_json(json_file,round_id):
    url = f"https://api.github.com/repos/G-r-ay/G-SSD/contents/archives/{round_id}_sybil_cluster.json"
    
    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3+json"
    }
    response = requests.get(url, headers=headers)
    response_json = response.json()
    existing_sha = response_json.get("sha")
    new_json_content_str = json.dumps(json_file, indent=4)


    payload = {
        "message": "Update sybil_clsuter json",
        "content": base64.b64encode(new_json_content_str.encode()).decode(),
        "sha": existing_sha
    }

    response = requests.put(url, json=payload, headers=headers)

    if response.status_code == 200:
        print("JSON file updated successfully.")
    else:
        print("Failed to update JSON file.")
#---------------------------------------------------------------------------------------------------------------
def update_round_time_data(round_id,new_data):
    existing_file_url = f'https://raw.githubusercontent.com/G-r-ay/G-SSD/main/archives/{round_id}_time.parquet'
    data = pd.read_parquet(existing_file_url)
    data.dropna(inplace=True)
    df = pd.concat([data, new_data], ignore_index=True)


    df.drop_duplicates(inplace=True)
    modified_content = df.to_parquet(index=False)
    modified_content_encoded = base64.b64encode(modified_content).decode()

    api_url = f'https://api.github.com/repos/G-r-ay/G-SSD/contents/archives/{round_id}_time.parquet'

    headers = {
        "Authorization": f"Bearer {github_token}"
    }

    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        file_info = response.json()
        payload = {
            "message": "Update Parquet file",
            "content": modified_content_encoded,
            "sha": file_info["sha"]
        }

        update_response = requests.put(api_url, json=payload, headers=headers)
        if update_response.status_code == 200:
            print("File updated date successfully.")
        else:
            print("Error updating file:", update_response.text)
    else:
        print("Error getting file info:", response.text)





