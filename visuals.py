import streamlit as st
import json
import locale
import pandas as pd
import random
import requests
from upkeep import checkUpKeep
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import plotly.express as px


palette = ['#05668D', '#028090', '#00A896', '#02C39A']
background_color = "#f0f0f0"
shadow_color = "rgba(0, 0, 0, 0.2)"


st.set_page_config(page_title="Cluster Visualization with Top Bar",layout='wide')

selected_round = st.sidebar.title('G_SSD')


selected_round = st.sidebar.selectbox(
    "Select A Round",
    ("Climate Round", "Web3 Open Source Software","Web3 Community and Education")
)

if selected_round == 'Climate Round':
    round_id = '0xb6Be0eCAfDb66DD848B0480db40056Ff94A9465d'
elif selected_round == 'Web3 Open Source Software':
    round_id = '0x8de918F0163b2021839A8D84954dD7E8e151326D'
else:
    round_id = '0x2871742B184633f8DC8546c6301cbC209945033e'


data_main = checkUpKeep(round_id)
voter_data = data_main.drop_duplicates(subset='voter')
url = f"https://raw.githubusercontent.com/G-r-ay/G-SSD/main/archives/{round_id}_sybil_cluster.json"
response = requests.get(url)
json_data = response.json()
print(json_data)


st.markdown('<link rel="stylesheet" href="styling.css">', unsafe_allow_html=True)
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
top_bar_style = """
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    height: 50px;
    background-color: #ffffff;
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 100;
"""

st.markdown(
    f'<div style="{top_bar_style}">hello</div>',
    unsafe_allow_html=True
)
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
col1, col2, col3, col4 = st.columns(4)

with col1:
    box_style = f"""
        padding: 5px;
        background-color: {palette[0]};
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.3);
        text-align: left;
    """
    try:
        num_sybils = voter_data['status'].value_counts()['Sybil']
    except KeyError:
        num_sybils = 0
    st.markdown(f'<div style="{box_style}"><p style="color: white; padding-left: 10px;">Total Number Of Identified Sybils</p><h2 style="padding-left: 10px;color: white;"><b>{num_sybils}</b></h2></div>', unsafe_allow_html=True)
with col2:
    box_style = f"""
        padding: 5px;
        background-color: {palette[1]};
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.3);
        text-align: left;
    """
    sybil_data = data_main.loc[data_main['status']=='Sybil']['amountUSD'].sum()

    sybils_donations_sum = "${:,.2f}".format(sybil_data)
    st.markdown(f'<div style="{box_style}"><p style="color: white; padding-left: 10px;">Amount Donated By Sybils ($)</p><h2 style="padding-left: 10px;color: white;"><b>{sybils_donations_sum}</b></h2></div>', unsafe_allow_html=True)
with col3:
    box_style = f"""
        padding: 5px;
        background-color: {palette[2]};
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.3);
        text-align: left;
    """

    unique_voters = data_main.drop_duplicates('voter')
    class_counts = unique_voters['status'].value_counts()
    desired_class_count = class_counts.get('Sybil', 0)
    total_instances = len(unique_voters)
    sybil_percentage = (desired_class_count / total_instances) * 100
    sybil_percentage = "{:,.2f}".format(sybil_percentage)
    st.markdown(f'<div style="{box_style}"><p style="color: white; padding-left: 10px;">Percentage of Sybil Voters</p><h2 style="padding-left: 10px;color: white;"><b>{sybil_percentage}%</b></h2></div>', unsafe_allow_html=True)
with col4:
    box_style = f"""
        padding: 5px;
        background-color: {palette[3]};
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.3);
        text-align: left;
    """

    max_key = None
    max_length = 0

    # Iterate through the dictionary's keys and values
    for cluster, value in data_json.items():
        if len(value) > max_length:
            max_key = cluster
            max_length = len(value)
    subscript = '<sup>EOA</sup>'
    st.markdown(f'<div style="{box_style}"><p style="color: white; padding-left: 10px;">Largest Cluster Size</p><h2 style="padding-left: 10px;color: white;"><b>{max_length}</b> {subscript}</h2></div>', unsafe_allow_html=True)

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
with st.container():
    date_range = pd.date_range(start='2023-01-01', periods=10, freq='D')
    data = {
        'Time': date_range,
        'Area 1': np.random.randint(10, 100, size=10),
        'Area 2': np.random.randint(20, 120, size=10)
    }
    data = pd.DataFrame(data)

    fig = px.area(data, x='Time', y=['Area 1', 'Area 2'], color_discrete_sequence=[palette[1], palette[3]],title='Votes Over Time')
    fig.update_layout(title_x=0.45)


    fig.update_traces(opacity=0.5) 

    fig.update_layout(plot_bgcolor='#FFFFFF', paper_bgcolor='#FFFFFF')

    st.markdown(f"""
        <style>
            .stPlotlyChart {{
                background-color: {background_color};
                box-shadow: 0px 4px 10px {shadow_color};
                overflow: hidden;
            }}
        </style>
        """, unsafe_allow_html=True)

    st.plotly_chart(fig,use_container_width=True)

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

col1, col2 = st.columns([60, 40])

with col1:

    pivot_data = data_main.pivot_table(index='status', columns='project_title', aggfunc='size', fill_value=0)

    # Get the list of categories (statuses)
    pivot_data = pivot_data.sort_values(by='Sybil', axis=1, ascending=False)
    categories = pivot_data.index.tolist()
    data_values = pivot_data.values
    data_values = [np.array(row) for row in data_values]
    categories = categories[:15]
    # Get the list of subcategories (project_titles)
    subcategories = [x for _, x in sorted(zip(data_values[1], pivot_data.columns.tolist()), reverse=False)]


    subcategories = [title[:20] for title in subcategories][:15]

    data_values = sorted(data_values, key=lambda x: -np.sum(x))
    subcategories = sorted(subcategories, reverse=True)
    color_palette = [palette[-3], palette[-2]]
    fig = go.Figure()

    for idx, category in enumerate(categories):
        fig.add_trace(go.Bar(
            y=subcategories,
            x=data_values[idx],
            name=category,
            orientation='h',
            marker_color=color_palette[idx],
        ))



    fig.update_layout(
        barmode='stack',
        title='Projects Votes Distribution',
        margin=dict(t=50, b=20, l=10, r=10),
        plot_bgcolor='#FFFFFF', paper_bgcolor='#FFFFFF',
        legend=dict(orientation="h", yanchor="top", xanchor="center", x=0.45, y=-0.2),
        xaxis=dict(ticklen=10, tickfont=dict(size=12), showgrid=True, gridwidth=1, gridcolor='rgba(0,0,0,0.1)'),
        yaxis=dict(ticklen=15, tickfont=dict(size=12), showgrid=False),
        yaxis_ticklen=15,
        yaxis_categoryorder='category ascending'
    )
    fig.update_layout(title_x=0.45)

    st.markdown(f"""
    <style>
        .stPlotlyChart {{
            border-radius: 15px;
            background-color: {background_color};
            box-shadow: 0px 4px 10px {shadow_color};
            overflow: hidden;
        }}
    </style>
    """, unsafe_allow_html=True)

    st.plotly_chart(fig,use_container_width=True)
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

with col2:


    try:
        Sybils = voter_data['status'].value_counts()['Sybil']
    except KeyError:
        Sybils = 0
    Non_Sybils = voter_data['status'].value_counts()['Non-Sybil']
    num_nodes = Sybils + Non_Sybils
    theta = np.random.uniform(0, np.pi, num_nodes)
    phi = np.random.uniform(0, 2 * np.pi, num_nodes)
    x = np.sin(theta) * np.cos(phi)
    y = np.sin(theta) * np.sin(phi)
    z = np.cos(theta)


    center_x = [0]
    center_y = [0]
    center_z = [0]

    fig = go.Figure()

    fig.add_trace(go.Scatter3d(x=center_x, y=center_y, z=center_z, mode='markers', marker=dict(size=5, color=palette[0])))
    fig.add_trace(go.Scatter3d(x=x[:Sybils], y=y[:Sybils], z=z[:Sybils], mode='markers', marker=dict(size=2, color="#FF5733")))
    fig.add_trace(go.Scatter3d(x=x[Sybils:], y=y[Sybils:], z=z[Sybils:], mode='markers', marker=dict(size=2, color="#3ACDD4")))

    fig.update_layout(scene=dict(aspectmode="auto", xaxis_showgrid=False, yaxis_showgrid=False, zaxis_showgrid=False))
    fig.update_layout(scene=dict(xaxis=dict(showticklabels=False), yaxis=dict(showticklabels=False), zaxis=dict(showticklabels=False)))
    fig.update_layout(scene=dict(xaxis_title='', yaxis_title='', zaxis_title=''))
    fig.update_layout(scene=dict(xaxis_visible=False, yaxis_visible=False, zaxis_visible=False))
    fig.update_layout(showlegend=False)
    fig.update_layout(plot_bgcolor='#FFFFFF', paper_bgcolor='#FFFFFF', height=450)
    start_view_angle = dict(
        eye=dict(x=0.95, y=0.95, z=0.4)
    )
    fig.update_layout(margin=dict(l=0, r=0, t=60, b=20))
    fig.update_layout(scene_camera=start_view_angle)
    fig.update_layout(title="Globe Representataion")
    fig.update_layout(title_x=0.34)

    st.markdown(f"""
    <style>
        .stPlotlyChart {{
            border-radius: 15px;
            background-color: {background_color};
            box-shadow: 0px 4px 10px {shadow_color};
            overflow: hidden;
        }}
    </style>
    """, unsafe_allow_html=True)

    st.plotly_chart(fig, use_container_width=True)

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

cluster_container = st.container()
with cluster_container:
    nodes = []
    y_coordinates = []

    for cluster, points in data_json.items():
        nodes.append({"id": cluster, "size": len(points)})
        y_coordinates.append(random.random())

    color_scale = ['#05668D', '#0E7C9D', '#198FB0', '#29AFC2', '#3ACDD4', '#4BE8E6']

    fig = go.Figure()

    for node, y_coord in zip(nodes, y_coordinates):
        cluster_size = node["size"]
        color_index = min(cluster_size // 5, len(color_scale) - 1)  # Determine color index based on cluster size
        node_color = color_scale[color_index]

        fig.add_trace(
            go.Scatter(

                x=[node["id"]],
                y=[y_coord],
                mode="markers",
                marker=dict(size=node["size"], sizemode="diameter", color=node_color),  # Use the determined color
                text=node["size"],
            )
        )

    fig.update_layout(
        title="Network Graph",
        showlegend=False,
        xaxis=dict(showline=False, showticklabels=False, showgrid=False),
        plot_bgcolor='#FFFFFF', paper_bgcolor='#FFFFFF',
        yaxis=dict(showline=False, showticklabels=False, showgrid=False),
        height=500,
    )
    fig.update_layout(margin=dict(l=0, r=0, t=75, b=0))

    fig.update_layout(title_x=0.46)

    fig.update_layout(
        hoverlabel=dict(
            bgcolor=background_color,
            font_color="black",
            bordercolor=shadow_color,
        ),
        hovermode="closest",
    )

    st.plotly_chart(fig, use_container_width=True)

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
col1,col2 = st.columns([30 ,55])

with col2:

    # Calculate the sum of amountUSD for each project_title (category)
    data = data_main.loc[data_main['status']=='Sybil']
    grouped_df = data.groupby('project_title')['amountUSD'].sum().reset_index()

    # Create a Treemap plot using Plotly
    fig = px.treemap(grouped_df, 
                    path=['project_title'], 
                    values='amountUSD', 
                    title='Treemap Example')

    # Update layout for Plotly figure
    fig.update_layout(
        title="Sybil Funding Treemap",
        plot_bgcolor='#FFFFFF',
        paper_bgcolor='#FFFFFF',
        margin=dict(l=0, r=0, t=60, b=0),
        title_x=0.42
    )

    # Custom CSS styles for the Plotly chart
    background_color = "#F7F7F7"
    shadow_color = "#AAB7B8"
    st.markdown(f"""
    <style>
        .stPlotlyChart {{
            border-radius: 15px;
            background-color: {background_color};
            box-shadow: 0px 4px 10px {shadow_color};
            overflow: hidden;
        }}
    </style>
    """, unsafe_allow_html=True)

    # Display the Plotly chart in Streamlit
    st.plotly_chart(fig, use_container_width=True)

with col1:
    labels = ['Sybil', 'Non-Sybil']

    try:
        Sybils = voter_data['status'].value_counts()['Sybil']
    except KeyError:
        Sybils = 0
    Non_sybils = voter_data['status'].value_counts()['Non-Sybil']
    values = [Sybils, Non_sybils]  # Adjust the values as needed
    colors = ['#00A896', '#02C39A']  # Define your two desired colors

    # Create the Plotly donut plot
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.6, marker=dict(colors=colors),textinfo='none')])

    # Add value annotation in the center
    center_text = f'<b>{sum(values)}</b><br>Total Votes'
    fig.update_layout(
        title='Votes Percentages',
        margin=dict(t=60, b=100, l=60, r=60),
        legend=dict(orientation="h", yanchor="bottom", xanchor="center", x=0.5, y=-0.3),  # Adjust margins as needed
        annotations=[dict(text=center_text, showarrow=False, x=0.5, y=0.5)],
        font=dict(size=14)
    )
    fig.update_layout(title_x=0.34)
    fig.update_layout(plot_bgcolor='#FFFFFF', paper_bgcolor='#FFFFFF')
    st.markdown(f"""
    <style>
        .stPlotlyChart {{
            border-radius: 15px;
            background-color: {background_color};
            box-shadow: 0px 4px 10px {shadow_color};
        }}
    </style>
    """, unsafe_allow_html=True)
    # Display the chart using Streamlit
    st.plotly_chart(fig,use_container_width=True)

