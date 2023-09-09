import streamlit as st
from datetime import datetime


# By James C. Hu
# Streamlit dashboard landing page.

date = datetime.today().strftime('%b-%d-%Y')

st.set_page_config(
    page_title='Weekly GISAID update',
    page_icon='👋',
)

st.write('# COVIDSeq Update')
st.markdown(f'#### {date}')

st.sidebar.success('Select a page above.')

st.markdown(
    '''
    This dashboard contains the most recent data on circulating sever acute respiratory syndrome coronavirus 2 (SARS-CoV-2) lineages in Arizona.

    **👈 Select a page from the sidebar** to see interactive visualizations and data.

    #### A Brief Overview of [SARS-CoV-2](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7173023/)
    SARS-CoV-2 is the zoonotic RNA virus responsible for the most recent global calamity spanning from late December of 2019 to today.
    Theories regarding the origin and evolution of this virus have converged on the most common natrual reservour for viruses of this genus - Bats!🦇

    SARS-CoV-2 belongs to the family and genus Coronaviridae and Beta-coronavirus. SARS-CoV-2 is an envloped, positive-sense, single-stranded, RNA virus (+ssRNA) with a genome of approximately 29.9kbs.
    Its viral [genome](https://www.nature.com/articles/s41586-020-2739-1) contains 14 open reading frames which code for 31 different protiens.
    They including four structural protiens (N, S, E, M), 16 non-structural protiens (nsp1-16), and 11 accessory proteins (ORF3a-d, ORF6, ORF7a-b, ORF8, ORF9b-c and ORF10).

'''
)

hide_streamlit_style = """
                <style>
                footer {
                visibility: hidden;
                height: 0%;
                }
                </style>
                """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
