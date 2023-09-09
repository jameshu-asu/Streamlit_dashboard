from helper_functions import *
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import datetime
from datetime import datetime as dt
import plotly.io as pio

# By James C. Hu
# This page displays the SARS-CoV-2 spike amino acid mutation tracker.


st.set_page_config(
    page_title='Spike Mutation Tracker',
    page_icon='🦠',
    layout='wide'
)

st.markdown('# SARS-CoV-2 Spike Protein Mutation')
st.markdown(f"#### Today's Date: {date1}")
st.markdown(f'#### Last Updated: {spike_mutation_tracker}')
st.markdown('---')
st.sidebar.header('Spike Protein Mutation Tracker')
st.write(
    '''
    ### About this page
    The interactive visualizations below displays SARS-CoV-2 spike protein amino acid mutations.

    The SARS-CoV-2 spike protein has been extenisvely studied throughout the pandemic due to its role in host cell [receptor recognition](https://www.nature.com/articles/s41586-020-2179-y) and infection.
    Certain key mutations within this gene can contribute to rapid [evolution](https://www.nature.com/articles/s41579-021-00573-0) and [spread](https://www.mdpi.com/1422-0067/24/3/2264) of the virus.

    The data displayed on this page was gathered from GISAID.org. The data reflects the prevalence of SARS-CoV-2 spike protein mutations in samples collected in Arizona within the last 90 days.
    '''
)

colors = ['#1f77b4', '#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c',
          '#98df8a', '#d62728', '#ff9896', '#9467bd', '#c5b0d5',
          '#8c564b', '#c49c94', '#e377c2', '#f7b6d2', '#7f7f7f',
          '#c7c7c7', '#bcbd22', '#dbdb8d', '#17becf', '#9edae5',
          '#cccccc', '#999999']


@st.cache_data
def getDataSpike():
    df = pd.read_csv('data/spike_mutation_tracker/output_mutation_tally_230320.csv')
    df = df.set_index('REFERENCE')
    return df


@st.cache_data
def getDataRBD():
    df = pd.read_csv('data/spike_mutation_tracker/output_mutation_tally_230320.csv')
    df = df.loc[332:526].copy()
    df = df.set_index('REFERENCE')
    return df


@st.cache_data
def getDataRBM():
    df = pd.read_csv('data/spike_mutation_tracker/output_mutation_tally_230320.csv')
    df = df.loc[437:505].copy()
    df = df.set_index('REFERENCE')
    return df


df = getDataSpike()
df2 = getDataRBD()
df3 = getDataRBM()

p = px.bar(df,
           color_discrete_sequence=colors,
           # color='variable',
           # text='variable', # get feedback
           title='SARS-CoV-2 Spike Protein Mutations',
           labels={
               'value': 'Number of Genomes',
               'REFERENCE': 'Mutations',
               'variable': 'Amino Acid'},
           # template='plotly_dark'
           )

p2 = px.bar(df2,
            color_discrete_sequence=colors,
            # color='variable',
            # text='variable', # get feedback
            title='SARS-CoV-2 Spike Protein RBD Mutations',
            labels={
                'value': 'Number of Genomes',
                'REFERENCE': 'Mutations',
                'variable': 'Amino Acid'},
            # template='plotly_dark'
            )

p3 = px.bar(df3,
            color_discrete_sequence=colors,
            # color='variable',
            # text='variable', # get feedback
            title='SARS-CoV-2 Spike Protein RBM Mutations',
            labels={
                'value': 'Number of Genomes',
                'REFERENCE': 'Mutations',
                'variable': 'Amino Acid'},
            # template='plotly_dark'
            )


p.update_layout(
    # hovermode='x', # get feedback
    # hovermode='x unified', # get feedback
    xaxis=dict(
        tickangle=-45,
    ),
    autosize=True,
)

p2.update_layout(
    # hovermode='x', # get feedback
    # hovermode='x unified', # get feedback
    xaxis=dict(
        tickangle=-45,
    ),
    autosize=True,
)

p3.update_layout(
    # hovermode='x', # get feedback
    # hovermode='x unified', # get feedback
    xaxis=dict(
        tickangle=-45,
    ),
    autosize=True,
)

uploaded_file = st.sidebar.file_uploader('Choose a FASTA file')
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    st.write(bytes_data)

    # To convert to a string based IO:
    stringio = StringIO(uploaded_file.getvalue().decode('utf-8'))
    st.write(stringio)

    # To read file as string:
    string_data = stringio.read()
    st.write(string_data)

    # Can be used wherever a 'file-like' object is accepted:
    dataframe = pd.read_csv(uploaded_file)
    st.write(dataframe)

s_date = datetime.date(2019, 1, 1)
e_date = datetime.date(2023, 1, 1)

start_date = st.sidebar.date_input(
    'Select start of date range', s_date)
st.sidebar.write('Date range starts at:', start_date)

end_date = st.sidebar.date_input(
    'Select end of date range', e_date)
st.sidebar.write('Date range ends at:', end_date)

st.plotly_chart(p, use_container_width=True)
st.plotly_chart(p2, use_container_width=True)
st.plotly_chart(p3, use_container_width=True)


# Add text between ''' and '''
# st.write(
#     '''
#     '''
# )
# p.show()
# p2.show()
# p3.show()

hide_streamlit_style = """
                <style>
                footer {
                visibility: hidden;
                height: 0%;
                }
                </style>
                """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
