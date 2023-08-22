import numpy as np
import json
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler
address = set()


def address_similarity(cultivated_data_citizen):
    MinMax = MinMaxScaler()
    data = MinMax.fit_transform(np.array(cultivated_data_citizen[cultivated_data_citizen.columns[1:]]))


    # Add supporterwallet column to data
    voter = cultivated_data_citizen['voter'].values.reshape(-1, 1)
    data = np.hstack((voter, data))

    similarity_matrix = cosine_similarity(data[:, 1:])
    # Set threshold for grouping together similar rows
    threshold = 0.7

    # Initialize list to store similar rows
    similar_rows = []

    # Loop through similarity matrix and group together similar rows
    for i in range(len(similarity_matrix)):
        similar_row_indices = np.where(similarity_matrix[i] >= threshold)[0]
        if len(similar_row_indices) > 1:
            similar_row_values = [tuple(cultivated_data_citizen.iloc[j])#i
                                for j in similar_row_indices]
            if similar_row_values not in similar_rows:
                similar_rows.append(similar_row_values)


    # Print out the similar rows
    import json

    similar_rows_json = {}

    # Loop through similarity matrix and group together similar rows
    for i, row_group in enumerate(similar_rows):
        cluster_group = []
        for row in row_group:
            cluster_group.append(row[0])
            if row[0] not in address:
                address.add(row[0])
        similar_rows_json[f"Cluster Group {i}"] = cluster_group

    # Serialize the similar_rows_json to a JSON file
    with open('archives/sybil_clusters.json', 'w') as file:
        json.dump(similar_rows_json, file,indent=1)
    return address
