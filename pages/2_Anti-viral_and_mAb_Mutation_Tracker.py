from helper_functions import *
import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime
import plotly.express as px
pd.options.display.width = 0

# By James C. Hu
# This dashboard page displays the SARS-CoV-2 anti-viral mutation tracker.


st.set_page_config(
    page_title='Mutation Tracker',
    page_icon='📈',
    layout='wide'
)

st.markdown('# SARS-CoV-2 Mutation Tracker')
st.markdown(f"#### Today's Date: {date1}")
st.markdown(f'#### Last Updated: {GISAID_update_date}')
st.markdown('---')
st.sidebar.header('Mutation Tracker')
st.write(
    '''
    ### About this page
    The interactive visualizations below displays SARS-CoV-2 mutations of public health interest and their prevalence by week.

    Mutations within the SARS-CoV-2 genome can enhance viral fitness, allowing for increased rates of escape from both diagnostic tools and the host's immune system.
    This phenomena translates to increased negative health outcomes for both the individuals afflicted by Covid-19, and the communities they reside in.
    Therefore, vigilant surveillance of circulating SARS-CoV-2 linages and their emerging mutations is of utmost importance in the continued managment of the disease.


    ##### Other Resources
    - Brief overview of antivirals, and [resistance mutations](https://www.science.org/content/blog-post/paxlovid-resistance-it-just-matter-time-now).
    - SARS-CoV-2 mutations that enhance viral fitness towards the Pfizer antiviral, [Paxlovid](https://www.sciencedirect.com/science/article/pii/S0753332223001555).
        - Paxlovid resistance cont. [1](https://www.nature.com/articles/s41586-022-05514-2), [2](https://www.biorxiv.org/content/10.1101/2022.06.28.497978v1), [3](https://pubs.acs.org/doi/10.1021/acs.jmedchem.2c00404), [4](https://www.biorxiv.org/content/10.1101/2022.06.28.497978v1), [5](https://www.biorxiv.org/content/10.1101/2022.07.02.495455v1).
    - SARS-CoV-2 mutations that enhance viral fitness towards [monoclonal antibodies](https://www.nature.com/articles/s41579-022-00809-7).
    - Host immune response after antibody treatment and its affect on SARS-CoV-2 [mutations](https://www.jci.org/articles/view/166032).

    '''
)


@st.cache_data
def getData1():
    df = pd.read_csv('data/mAb_resistance_tracker/raw_updated_parsed_mutations.csv')
    df = df.set_index('Week')
    df = df.drop(columns=['Counts'])
    df = df.iloc[1:, :]
    return df


@st.cache_data
def getData2():
    df = pd.read_csv('data/mAb_resistance_tracker/cleaned_updated_parsed_mutations.csv')
    df['Week'] = pd.to_datetime(df['Week'])
    df['Week'] = [datetime.strptime(
        str(x), '%Y-%m-%d').strftime('%b-%d-%Y') for x in df['Week'].dt.date]
    df = df.iloc[1:, :]
    return df


@st.cache_data
def getData3():
    df = pd.read_csv('data/mAb_resistance_tracker/cleaned_updated_parsed_mutations.csv')
    df = df.set_index('Week')
    df = df.T
    df = df.reset_index()
    df = df.rename(columns={'index': 'Mutation'})
    df = df.sort_values(by=df.columns[-1], ascending=False)
    return df


df = getData1()
df2 = getData2()
df3 = getData3()

mutation_list = [i for i in df3['Mutation']]

mutation_select = st.multiselect(
    'Choose a mutatiton',
    options=mutation_list,
    default=mutation_list[0:5],
)

df3_selection = df3.query(
    'Mutation == @mutation_select'
)

try:
    if not mutation_select:
        st.error('Please select at least one mutation.')
    else:
        mutation_chart = px.line(df3_selection.set_index('Mutation').T).update_layout(
            yaxis_title='Cumulative Count')
        mutation_chart.update_xaxes(tickangle=-45)
        st.subheader('Cumulative mutation count by week')
        st.plotly_chart(mutation_chart, use_container_width=True)
except Exception:
    st.error('Please select at least one mutation.')

# KPI's
cumulative_muation_count = df3_selection.sum(axis=0).iloc[-1]
highest_count_mutation = df3_selection.set_index('Mutation').idxmax().iloc[-1]
highest_count_mutation_count = df3_selection.max().iloc[-1]

st.subheader('Quick View')
st.markdown('---')
left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader(f'Total mutation count: [{cumulative_muation_count}]')
with middle_column:
    st.subheader(f'Most prevalent mutation: [{highest_count_mutation}]')
with right_column:
    st.subheader(
        f'{highest_count_mutation} count: [{highest_count_mutation_count}]')

# ------- Main --------
st.markdown('##### Mutation count by week')
st.dataframe(df.tail(5))
st.markdown('##### Cumulative mutation count by week')
st.dataframe(df2.set_index('Week').tail(1))

# print(cumulative_muation_count)
# print(highest_count_mutation)
# print(highest_count_mutation_count)

st.markdown('---')

hide_streamlit_style = """
                <style>
                footer {
                visibility: hidden;
                height: 0%;
                }
                </style>
                """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
