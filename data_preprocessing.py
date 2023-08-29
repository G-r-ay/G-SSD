import pandas as pd
from sklearn.preprocessing import  LabelEncoder
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def getData(round_id,tx_hash=False):
    data = pd.read_json(f'https://indexer-grants-stack.gitcoin.co/data/10/rounds/{round_id}/applications.json')
    projects = {}
    for _, row in data.iterrows():
        project_id = row['metadata']['application']['recipient']
        projects[project_id] = row['metadata']['application']['project']['title']

    votes = pd.read_json(f'https://indexer-grants-stack.gitcoin.co/data/10/rounds/{round_id}/votes.json')
    votes['project_title'] = votes['grantAddress'].map(projects)
    if tx_hash == False:
        votes.drop(['id','transaction','blockNumber','applicationId','roundId','grantAddress','token','amount','amountRoundToken'],axis=1,inplace=True)
        votes.dropna(inplace=True)
        return votes
    else:
        votes.drop(['id','blockNumber','applicationId','roundId','grantAddress','token','amount','amountRoundToken'],axis=1,inplace=True)
        votes.dropna(inplace=True)
        return votes
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def preprocess_data(round_data:pd.DataFrame):
    funding_counts = round_data['voter'].value_counts()

    count_by_address_project = round_data.groupby(
        ['voter', 'project_title']).size().reset_index(name='count')
    no_grants_funded = count_by_address_project['voter'].value_counts()

    voter_funding_counts = pd.DataFrame({'voter': funding_counts.index, 'Funding_count': funding_counts.values})
    voter_no_grants_funded = pd.DataFrame({'voter': no_grants_funded.index, 'No_Projects_Funded': no_grants_funded.values})

    Address_info = pd.merge(voter_funding_counts, voter_no_grants_funded)

    filtered_round_data = pd.merge(Address_info, round_data, how='left', on='voter')

    data_points = ['voter', 'Funding_count', 'No_Projects_Funded']

    filtered_round_data['address'] = filtered_round_data['voter']

    filtered_round_data['project_title_sorted'] = filtered_round_data['project_title'].apply(
        lambda x: '-'.join(sorted(x.lower().split())))
    df_result = filtered_round_data.groupby('address').agg({'voter': 'first',
                                                    'project_title_sorted': '_'.join}).reset_index()
    df_result = df_result.sort_values(by='project_title_sorted', ascending=False)[
        ['voter', 'project_title_sorted']]

    cut_filtered_data = filtered_round_data[data_points].drop_duplicates(subset=[
                                                                        'voter'])
    cut_filtered_data['voter'] = cut_filtered_data['voter']

    cultivated_data = pd.merge(
        cut_filtered_data, df_result, on='voter', how='left')
    cultivated_data = cultivated_data.loc[(cultivated_data['No_Projects_Funded'] <= 10) & (cultivated_data['Funding_count'] <= 10)]\
        .reset_index(drop=True)
    return cultivated_data

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def merger(user_data:pd.DataFrame,cultivated_data:pd.DataFrame):
    cultivated_data = pd.merge(cultivated_data, user_data, on='voter')
    columns_to_encode = ['project_title_sorted',
                        'first_from', 'first_to', 'last_from', 'last_to']
    for col in columns_to_encode:
        le = LabelEncoder()
        cultivated_data[col] = le.fit_transform(cultivated_data[col])
    return cultivated_data

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def label_dataframe(round_data,address):
    round_data['status'] = round_data['voter'].apply(lambda addr: 'Sybil' if addr in address else 'Non-Sybil')
    return round_data

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

