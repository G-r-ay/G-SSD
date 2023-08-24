import numpy as np
import json
from update_db import overwrite_github_json
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler
address = set()

#---------------------------------------------------------------------------------------------------------------

def address_similarity(full_data,round_id):
    MinMax = MinMaxScaler()
    data = MinMax.fit_transform(np.array(full_data[full_data.columns[1:]]))

    voter = full_data['voter'].values.reshape(-1, 1)
    data = np.hstack((voter, data))
    similar_rows_json = {}
    similarity_matrix = cosine_similarity(data[:, 1:])

    threshold = 0.999

    similar_rows = []

    for i in range(len(similarity_matrix)):
        similar_row_indices = np.where(similarity_matrix[i] >= threshold)[0]
        if len(similar_row_indices) > 1:
            similar_row_values = [tuple(full_data.iloc[j])#i
                                for j in similar_row_indices]
            if similar_row_values not in similar_rows:
                similar_rows.append(similar_row_values)

    # for i, row_group in enumerate(similar_rows):
    #     print(f"Similar Row Group {i}:")
    #     for row in row_group:
    #         print(row[0], row[1:])
    #     print()

    for i, row_group in enumerate(similar_rows):
        cluster_group = []
        for row in row_group:
            cluster_group.append(row[0])
            if row[0] not in address:
                address.add(row[0])
        similar_rows_json[f"Cluster Group {i}"] = cluster_group

    overwrite_github_json(similar_rows_json,round_id)
    return address
#---------------------------------------------------------------------------------------------------------------
