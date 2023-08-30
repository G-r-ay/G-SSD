import time
import requests
import numpy as np
import pandas as pd
from getter import *
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from upkeep import checkVotersUpKeep,date_up_keep_update

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#State Variables
palette = ['#BFC0C0','#2D3142']
round_status = 'finished'
background_color = "#f0f0f0"
shadow_color = "rgba(0, 0, 0, 0.2)"

if 'last_refresh_time' not in st.session_state:
    st.session_state.last_refresh_time = None

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#page configurations
st.set_page_config(page_title="G-SSD",layout='wide',page_icon='imgs/G-SSD.png')
st.sidebar.title('G_SSD')
st.sidebar.markdown(
    """
    <style>
    .sidebar-title {
        text-align: center;
        font-size: 24px;
        font-weight: bold;
        padding: 10px;
        margin-bottom: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)
# Page title
st.title("G-SSD: Gitcoin Sybil Summary Dashboard")

# Introduction
st.markdown("📊 **Introducing G-SSD: Unveiling Sybil's Impact!**\n\n"
            "Step into the world of decentralized collaboration with the Gitcoin Sybil Summary Dashboard (G-SSD). This powerful tool illuminates the often hidden effects of Sybil attacks on grant rounds and projects within the Gitcoin ecosystem, providing valuable insights for operators and voters alike.")

# Purpose
st.markdown("🎯 **Purpose**\n\n"
            "Sybil attacks pose a challenge to the integrity of decentralized networks. G-SSD addresses this challenge by presenting a clear visual representation of defense measures and their impact, making complex data easily understandable for everyone.")

# Empowering Community
st.markdown("🌟 **Empowering Community**\n\n"
            "G-SSD goes beyond data – it's about building a stronger community. By offering a comprehensive view of Sybil attack effects, G-SSD enables operators to fine-tune their strategies and voters to see their influence. Join us in unraveling the story behind Sybil attacks and fortifying our decentralized landscape!")

#----------------------------

temp_update = st.sidebar.button("temp_Update", key="temp_update_button", help="Update Round data")

if temp_update:
    round_status = 'Active'

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#Defaults and Selections
if 'selected_round' not in st.session_state:
    st.session_state.round_id = '0xb6Be0eCAfDb66DD848B0480db40056Ff94A9465d'
    st.session_state.selected_round = "Climate Round"

# Define buttons
if st.sidebar.button("Climate Round", use_container_width=True):
    st.session_state.round_id = '0xb6Be0eCAfDb66DD848B0480db40056Ff94A9465d'
    st.session_state.selected_round = "Climate Round"

if st.sidebar.button("Web3 Open Source Software", use_container_width=True):
    st.session_state.round_id = '0x8de918F0163b2021839A8D84954dD7E8e151326D'
    st.session_state.selected_round = "Web3 Open Source Software"

if st.sidebar.button("Web3 Community and Education", use_container_width=True):
    st.session_state.round_id = '0x2871742B184633f8DC8546c6301cbC209945033e'
    st.session_state.selected_round = "Web3 Community and Education "
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#Defaults and Selections
round_id = st.session_state.round_id
round_name = st.session_state.selected_round
@st.cache_data
def get_cluster_json(round_id):
    url = f"https://raw.githubusercontent.com/G-r-ay/G-SSD/main/archives/{round_id}_sybil_cluster.json"
    response = requests.get(url)
    return response.json()

if round_status == 'Active':
    st.sidebar.write(f"Selected Round {st.session_state.selected_round}")
    update_button = st.sidebar.button("Update", key="update_button", help="Update Round data")

    if update_button:
        st.sidebar.write(f"Last Refresh Time {time.strftime('%Y-%m-%d %H:%M:%S')}")
        def get_round_voter_data(round_id): 
            dt = checkVotersUpKeep(round_status,round_id)
            return dt

        def load_time_data(round_id,sybil_addresses): 
            return date_up_keep_update(round_id,sybil_addresses)
        
        def get_cluster_json(round_id):
            url = f"https://raw.githubusercontent.com/G-r-ay/G-SSD/main/archives/{round_id}_sybil_cluster.json"
            response = requests.get(url)
            return response.json()
    else:
        @st.cache_data
        def get_round_voter_data(round_id): 
            dt = get_labelled_existing(round_id)
            return dt
        @st.cache_data
        def load_time_data(round_id,sybil_addresses): 
            return get_date_existing(round_id,sybil_addresses)
else:
    @st.cache_data
    def get_gr18_data():
        data = pd.read_parquet("https://github.com/G-r-ay/G-SSD/raw/main/archives/gg18_data.parquet")
        return data

    @st.cache_data
    def get_round_voter_data(round_id,data,round_name):
        round_data = data.loc[data['round_name']==round_name]
        return get_voter_data(round_data,round_id)

    
    @st.cache_data
    def get_round_voting_data(data,round_name,sybil_addresses):
        return label_dataframe(data.loc[data['round_name']==round_name],sybil_addresses)

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#Data Initalization
round_id = st.session_state.round_id
json_data = get_cluster_json(round_id)
if round_status=='Active':
    if st.session_state.last_refresh_time is not None:
        st.sidebar.write(f"Last Refresh Time: {st.session_state.last_refresh_time}")
    round_voter_data,sybil_addresses = get_round_voter_data(round_id)
    time_data = load_time_data(round_id,sybil_addresses)

else:
    round_name = st.session_state.selected_round
    gg18_data = get_gr18_data()
    print(round_name)
    round_voter_data,sybil_addresses = get_round_voter_data(round_id,gg18_data,round_name)
    print(round_voter_data.shape, round_name)
    round_voter_data = round_voter_data.drop_duplicates(subset='voter')
    print(round_voter_data['round_name'].unique(), round_name)
    time_data = get_round_voting_data(gg18_data,round_name,sybil_addresses)
    print(round_voter_data['round_name'].unique(), round_name)

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#top bar
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
    color: red;  /* Set text color to black */
"""
st.markdown(
    f'<div style="{top_bar_style}">G-SSD</div>',
    unsafe_allow_html=True
)
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
col1, col2,col3,col4= st.columns([20,20,20,20])
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
with col1:
    box_style = f"""
        border-radius: 10px;
        padding: 5px;
        background-color: {palette[0]};
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.3);
        text-align: left;
        height: 100px;
        font-size: 10vh;  /* Font size based on 10% of the container height */
    """
    try:
        num_sybils = round_voter_data['status'].value_counts()['Sybil']
    except KeyError:
        num_sybils = 0
    st.markdown(f'<div style="{box_style}"><p style="color: white; padding-left: 10px;">Total Number Of Identified Sybils</p><h3 style="padding-left: 10px;color: white;"><b>{num_sybils}</b></h3></div>', unsafe_allow_html=True)

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

with col2:
    box_style = f"""
        border-radius: 10px;
        padding: 5px;
        background-color: {palette[1]};
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.3);
        text-align: left;
        height: 100px;
        font-size: 10vh;  /* Font size based on 10% of the container height */
    """
    sybil_data = time_data.loc[time_data['status']=='Sybil']['amountUSD'].sum()

    sybils_donations_sum = "${:,.2f}".format(sybil_data)
    st.markdown(f'<div style="{box_style}"><p style="color: white; padding-left: 10px;">Amount Donated By Sybils ($)</p><h3 style="padding-left: 10px;color: white;"><b>{sybils_donations_sum}</b></h3></div>', unsafe_allow_html=True)

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

with col3:
    box_style = f"""
        border-radius: 10px;
        padding: 5px;
        background-color: {palette[0]};
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.3);
        text-align: left;
        height: 100px;
        font-size: 10vh;  /* Font size based on 10% of the container height */
    """
    unique_voters = round_voter_data.drop_duplicates('voter')
    class_counts = unique_voters['status'].value_counts()
    desired_class_count = class_counts.get('Sybil', 0)
    total_instances = len(unique_voters)
    sybil_percentage = (desired_class_count / total_instances) * 100
    sybil_percentage = "{:,.2f}".format(sybil_percentage)
    st.markdown(f'<div style="{box_style}"><p style="color: white; padding-left: 10px;">Percentage Of Sybil Voters</p><h3 style="padding-left: 10px;color: white;"><b>{sybil_percentage}%</b></h3></div>', unsafe_allow_html=True)

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

with col4:
    max_key = None
    max_length = 0

    for cluster, value in json_data.items():
        if len(value) > max_length:
            max_key = cluster
            max_length = len(value)
    subscript = '<sup>EOA</sup>'

    box_style = f"""
        border-radius: 10px;
        padding: 5px;
        background-color: {palette[1]};
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.3);
        text-align: left;
        height: 100px;
        font-size: 10vh;  /* Font size based on 10% of the container height */
    """

    st.markdown(f'<div style="{box_style}"><p style="color: white; padding-left: 10px;">Largest Cluster Size</p><h3 style="padding-left: 10px;color: white;"><b>{max_length}{subscript}</b></h3></div>', unsafe_allow_html=True)

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
treemap,time_ = st.columns([30,70])
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#Votes/Time
with time_:
    time_data['tx_timestamp'] = pd.to_datetime(time_data['tx_timestamp'])
    df_grouped = time_data.groupby([time_data['tx_timestamp'].dt.date, 'status']).size().unstack(fill_value=0).reset_index()
    df_long = df_grouped.melt(id_vars='tx_timestamp', value_vars=['Sybil', 'Non-Sybil'], var_name='status', value_name='count')
    fig = px.area(df_long, x='tx_timestamp', y='count', color='status', title='Sybil and Non-Sybil Votes per Day',color_discrete_sequence=['#2D3142','#BFC0C0'])

    fig.update_xaxes(type='category')
    fig.update_traces(mode='lines', stackgroup='one')
    fig.update_layout(plot_bgcolor='#FFFFFF', paper_bgcolor='#FFFFFF', height=500)
    fig.update_traces(mode='markers', opacity=0.7, line=dict(dash='dash'))
    fig.update_layout(plot_bgcolor='#FFFFFF', paper_bgcolor='#FFFFFF', height=500)

    st.markdown(f"""
        <style>
            .stPlotlyChart {{
                border-radius: 10px;
                background-color: {background_color};
                box-shadow: 0px 4px 10px {shadow_color};
                overflow: hidden;
            }}
        </style>
        """, unsafe_allow_html=True)

    st.plotly_chart(fig, use_container_width=True)

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#Funding map
with treemap:
    data = round_voter_data.loc[round_voter_data['status']=='Sybil']
    grouped_df = data.groupby('project_title')['amountUSD'].sum().reset_index()


    fig = px.treemap(grouped_df, 
                    path=['project_title'], 
                    values='amountUSD', 
                    title='Treemap Example',
                    color_discrete_sequence=['#1e1e24','#dddddd','#cccccc','#bbbbbb','#aaaaaa'])


    fig.update_layout(
        title="Sybil Funding Landscape: Top Projects Breakdown (USD)",
        plot_bgcolor='#FFFFFF',
        paper_bgcolor='#FFFFFF',
        margin=dict(l=0, r=0, t=40, b=0),
        height=500
    )


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

    st.plotly_chart(fig, use_container_width=True)

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
bar,pie = st.columns([70,30])
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

with bar:
    status_counts = time_data.groupby(['project_title', 'status']).size().reset_index(name='count')
    pivot_table = status_counts.pivot_table(index='project_title', columns='status', values='count', fill_value=0)
    pivot_table.reset_index(inplace=True)
    pivot_table.sort_values(by='Sybil',inplace=True, ascending=False)
    categories = pivot_table['project_title'].tolist()[:15]
    categories = [title[:20] for title in categories]
    data_values_non_sybil = pivot_table['Non-Sybil'].tolist()[:15]
    data_values_sybil = pivot_table['Sybil'].tolist()[:15]


    color_palette = [palette[0], palette[1]]

    fig = go.Figure()


    fig.add_trace(go.Bar(
        y=categories,
        x=data_values_non_sybil,
        name='Non-Sybil',
        orientation='h',
        marker_color=color_palette[0],
    ))


    fig.add_trace(go.Bar(
        y=categories,
        x=data_values_sybil,
        name='Sybil',
        orientation='h',
        marker_color=color_palette[1],
    ))

    fig.update_layout(
        barmode='stack',
        title='Vote Comparison By Project',
        margin=dict(t=50, b=20, l=10, r=10),
        plot_bgcolor='#FFFFFF', paper_bgcolor='#FFFFFF',
        legend=dict(orientation="h", yanchor="top", xanchor="center", x=0.45, y=-0.2),
        xaxis=dict(ticklen=10, tickfont=dict(size=12), showgrid=True, gridwidth=1, gridcolor='rgba(0,0,0,0.1)'),
        yaxis=dict(ticklen=15, tickfont=dict(size=12), showgrid=False),
        yaxis_ticklen=15,
        yaxis_categoryorder='total ascending',
        height=500
    )


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

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

with pie:
    labels = ['Sybil', 'Non-Sybil']

    try:
        Sybils = round_voter_data['status'].value_counts()['Sybil']
    except KeyError:
        Sybils = 0
    Non_sybils = round_voter_data['status'].value_counts()['Non-Sybil']
    values = [Sybils,Non_sybils] 
    colors = [palette[1],palette[0]]  


    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.7, marker=dict(colors=colors),textinfo='none',showlegend=True)])

    center_text = f'<b>{sum(values)}</b><br>Total Voters'
    fig.update_layout(
        title='Votes Distribution: Sybil vs. Non-Sybil',
        margin=dict(t=80, b=60, l=80, r=80),
        legend=dict(orientation="h", yanchor="bottom", xanchor="center", x=0.5, y=-0.3), 
        annotations=[dict(text=center_text, showarrow=False, x=0.5, y=0.5)],
        font=dict(size=14)
    )
    
    fig.update_layout(plot_bgcolor='#FFFFFF', paper_bgcolor='#FFFFFF',height=500)
    st.markdown(f"""
    <style>
        .stPlotlyChart {{
            border-radius: 10px;
            background-color: {background_color};
            box-shadow: 0px 4px 10px {shadow_color};
        }}
    </style>
    """, unsafe_allow_html=True)

    st.plotly_chart(fig,use_container_width=True)

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
globe = st.container()
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
with globe:
    option = st.selectbox('Select a Project', time_data['project_title'].unique(), index=0, key='selectbox')
    project_data = round_voter_data.loc[round_voter_data['project_title'] == option]

    try:
        Sybils = project_data['status'].value_counts()['Sybil']
    except KeyError:
        Sybils = 0
    Non_Sybils = project_data['status'].value_counts()['Non-Sybil']
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
    fig.add_trace(go.Scatter3d(x=x[:Sybils], y=y[:Sybils], z=z[:Sybils], mode='markers', marker=dict(size=2, color='#773344')))
    fig.add_trace(go.Scatter3d(x=x[Sybils:], y=y[Sybils:], z=z[Sybils:], mode='markers', marker=dict(size=2, color=palette[0])))

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
    fig.update_layout(title="Voting Status Sphere: Sybil vs. Non-Sybil")


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

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
