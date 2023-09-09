from helper_functions import *
import pandas as pd
import numpy as np
import folium
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
from datetime import datetime
from streamlit_folium import st_folium
from PIL import Image

# By James C. Hu
# This page displays ASU Tempe campus wastewater data.


def HIGHLIGHTER(x: pd.Series):
    '''
    This function changes the color of each cell of the read distribution table based on criteria.
    '''
    median = int(round(x.median()))
    high_bar = median + int(round(0.5 * x.std()))

    def color_switch(number):
        color = ''
        if (number == 0) | (number < median):
            color = '#66bd63'  # green
        elif (number >= median) & (number < high_bar):
            color = '#fed976'  # yellow
        else:
            color = '#fb6a4a'  # red
        return color
    return[f'color: black; background-color: {color_switch(number)}' for number in x]


st.set_page_config(
    page_title='Tempe Campus',
    page_icon='🚱',
    layout='wide'
)

####_______FOLIUM_MAP_________####

# latitude and longitudes positions correspond with popups and tooltips in the same index position
latitudes_list = [33.452039, 33.453573, 33.418049, 33.452113, 33.453294,
                  33.452863, 33.446281, 33.445880, 33.445257, 33.444915,
                  33.442871, 33.442884, 33.446039, 33.444470, 33.445984,
                  33.449664, 33.449298, 33.442171, 33.448314, 33.448429]

longitudes_list = [-111.933943, -111.933783, -111.926203, -111.930186, -111.933761,
                   -111.933746, -111.929055, -111.930002, -111.930380, -111.928599,
                   -111.927151, -111.927948, -111.935788, -111.931554, -111.932021,
                   -111.935681, -111.936687, -111.928021, -111.934340, -111.933710]

popups = ['ASU Tempe: T1', 'ASU Tempe: T2', 'ASU Tempe: T3', 'ASU Tempe: T4', 'ASU Tempe: T5',
          'ASU Tempe: T6', 'ASU Tempe: T7', 'ASU Tempe: T8', 'ASU Tempe: T9', 'ASU Tempe: T10',
          'ASU Tempe: T11', 'ASU Tempe: T12', 'ASU Tempe: T14', 'ASU Tempe: T15', 'ASU Tempe: T16',
          'ASU Tempe: T17', 'ASU Tempe: T18', 'ASU Tempe: T19', 'ASU Tempe: T20', 'ASU Tempe: T21']

tooltips = ['T1', 'T2', 'T3', 'T4', 'T5',
            'T6', 'T7', 'T8', 'T9', 'T10',
            'T11', 'T12', 'T14', 'T15', 'T16',
            'T17', 'T18', 'T19', 'T20', 'T21']

# Center at latitude/longitude coordinates.
m = folium.Map(location=[33.459248, -111.930976], zoom_start=15)

# Add markers iteratively using the zipped lists.
for i, j, k, l in zip(latitudes_list, longitudes_list, popups, tooltips):
    iframe = folium.IFrame(k)
    folium.Marker(
        location=[i, j],
        popup=folium.Popup(iframe, min_width=275, max_width=275, min_height=50, max_height=50),
        tooltip=l,
        icon=folium.Icon(color='orange')

    ).add_to(m)


####_______FREYJA_ANALYSIS_________####
Freyja_infile = pd.read_csv('data/wastewater_virus_surveillance/combined/Combined_freyja_grouped_metadata_analysis.csv')

# set location for location codes and location specific read disttribution data.
LOCATION: Final = 'tempe'
LOCATION_ID: Final = 'ASUT'
SAMPLE_ID1: Final = 'AWW'
SAMPLE_ID2: Final = 'AWMT'

# reads from combined_freyja metadata file, sorts by campus location
# location_code Tempe: ASUT, Polytechnic: ASUP, West: ASUW, Downtown: ASUDT
df_freyja_sorted_tempe = freyja_sort_by_location(Freyja_infile, LOCATION_ID)
df_freyja_date = freyja_by_date(df_freyja_sorted_tempe)
# resetting index because merge function sets df index to "Date" and sort_df_date function needs "Date" to be in a column
df_freyja_date = df_freyja_date.reset_index()
df_freyja_date = sort_df_data(df_freyja_date).tail(16)

df_location = locations(LOCATION)
df_tempe_reads = read_distribution(LOCATION).tail(6)

#____Freyja_averaged_charts_____
df_melt1 = organize_df(df_freyja_date, 'Date')
# df_melt2 = organize_df(df_freyja_site, 'Site')
p_freyja_date = location_date_bar_graph(df_melt1, 'Date', 'Variant', 'ASU Tempe Wastewater SARS-CoV-2 Variants by Date', 500, 500)
# p_freyja_site = location_date_bar_graph(df_melt2, 'Site', 'ASU Tempe Wastewater SARS-CoV-2 Variants by Location')

#____Freyja_site_specific_charts____
df_site_date_freyja = freyja_sort_by_location(Freyja_infile, LOCATION_ID, 'area5', 'area1', 'area3', 'area2', 'area4')

# Initializing dfs for collection site specific SARS-CoV-2 variant abundance by colletion date data.
df_asu01_freyja = freyja_location_site_by_date(df_site_date_freyja, 'ASUT01')
df_asu02_freyja = freyja_location_site_by_date(df_site_date_freyja, 'ASUT02', 'area5')
df_asu03_freyja = freyja_location_site_by_date(df_site_date_freyja, 'ASUT03')
df_asu04_freyja = freyja_location_site_by_date(df_site_date_freyja, 'ASUT04')
df_asu05_freyja = freyja_location_site_by_date(df_site_date_freyja, 'ASUT05', 'area5')
df_asu06_freyja = freyja_location_site_by_date(df_site_date_freyja, 'ASUT06', 'area5')
df_asu07_freyja = freyja_location_site_by_date(df_site_date_freyja, 'ASUT07', 'area2')
df_asu08_freyja = freyja_location_site_by_date(df_site_date_freyja, 'ASUT08', 'area2')
df_asu09_freyja = freyja_location_site_by_date(df_site_date_freyja, 'ASUT09', 'area2')
df_asu10_freyja = freyja_location_site_by_date(df_site_date_freyja, 'ASUT10')
df_asu11_freyja = freyja_location_site_by_date(df_site_date_freyja, 'ASUT11', 'area1')
df_asu12_freyja = freyja_location_site_by_date(df_site_date_freyja, 'ASUT12', 'area1')
df_asu14_freyja = freyja_location_site_by_date(df_site_date_freyja, 'ASUT14', 'area4')
df_asu15_freyja = freyja_location_site_by_date(df_site_date_freyja, 'ASUT15')
df_asu16_freyja = freyja_location_site_by_date(df_site_date_freyja, 'ASUT16', 'area4')
df_asu17_freyja = freyja_location_site_by_date(df_site_date_freyja, 'ASUT17', 'area3')
df_asu18_freyja = freyja_location_site_by_date(df_site_date_freyja, 'ASUT18')
df_asu19_freyja = freyja_location_site_by_date(df_site_date_freyja, 'ASUT19')
df_asu20_freyja = freyja_location_site_by_date(df_site_date_freyja, 'ASUT20', 'area3')
df_asu21_freyja = freyja_location_site_by_date(df_site_date_freyja, 'ASUT21', 'area3')


# Initializing plotly express graph objects using the dfs above.
p1_freyja = location_date_bar_graph(df_asu01_freyja, 'Date', 'Variants', 'ASU Tempe T1', 500, 500)
p2_freyja = location_date_bar_graph(df_asu02_freyja, 'Date', 'Variants', 'ASU Tempe T2', 500, 500)
p3_freyja = location_date_bar_graph(df_asu03_freyja, 'Date', 'Variants', 'ASU Tempe T3', 500, 500)
p4_freyja = location_date_bar_graph(df_asu04_freyja, 'Date', 'Variants', 'ASU Tempe T4', 500, 500)
p5_freyja = location_date_bar_graph(df_asu05_freyja, 'Date', 'Variants', 'ASU Tempe T5', 500, 500)
p6_freyja = location_date_bar_graph(df_asu06_freyja, 'Date', 'Variants', 'ASU Tempe T6', 500, 500)
p7_freyja = location_date_bar_graph(df_asu07_freyja, 'Date', 'Variants', 'ASU Tempe T7', 500, 500)
p8_freyja = location_date_bar_graph(df_asu08_freyja, 'Date', 'Variants', 'ASU Tempe T8', 500, 500)
p9_freyja = location_date_bar_graph(df_asu09_freyja, 'Date', 'Variants', 'ASU Tempe T9', 500, 500)
p10_freyja = location_date_bar_graph(df_asu10_freyja, 'Date', 'Variants', 'ASU Tempe T10', 500, 500)
p11_freyja = location_date_bar_graph(df_asu11_freyja, 'Date', 'Variants', 'ASU Tempe T11', 500, 500)
p12_freyja = location_date_bar_graph(df_asu12_freyja, 'Date', 'Variants', 'ASU Tempe T12', 500, 500)
p14_freyja = location_date_bar_graph(df_asu14_freyja, 'Date', 'Variants', 'ASU Tempe T14', 500, 500)
p15_freyja = location_date_bar_graph(df_asu15_freyja, 'Date', 'Variants', 'ASU Tempe T15', 500, 500)
p16_freyja = location_date_bar_graph(df_asu16_freyja, 'Date', 'Variants', 'ASU Tempe T16', 500, 500)
p17_freyja = location_date_bar_graph(df_asu17_freyja, 'Date', 'Variants', 'ASU Tempe T17', 500, 500)
p18_freyja = location_date_bar_graph(df_asu18_freyja, 'Date', 'Variants', 'ASU Tempe T18', 500, 500)
p19_freyja = location_date_bar_graph(df_asu19_freyja, 'Date', 'Variants', 'ASU Tempe T19', 500, 500)
p20_freyja = location_date_bar_graph(df_asu20_freyja, 'Date', 'Variants', 'ASU Tempe T20', 500, 500)
p21_freyja = location_date_bar_graph(df_asu21_freyja, 'Date', 'Variants', 'ASU Tempe T21', 500, 500)


####_______RVP_ANALYSIS_________####
RVP_infile = pd.read_csv(f'data/wastewater_virus_surveillance/combined/RVP_counts_virusOnly_normalized_filled_{run}.csv')
RVP_infile2 = pd.read_csv(f'data/wastewater_virus_surveillance/tempe/rvp/RVP_counts_tempe_normalized_avg_groupby_date.csv', index_col=0)

#____RVP_site_specific_charts___
df_RVP_sorted_tempe = RVP_sort_by_location(RVP_infile, LOCATION_ID)

# Initializing dfs for collection site specific SARS-CoV-2 variant abundance by colletion date data.
df_asu01_RVP = RVP_location_site_by_date(df_RVP_sorted_tempe, 'ASUT01')
df_asu02_RVP = RVP_location_site_by_date(df_RVP_sorted_tempe, 'ASUT02', 'area5')
df_asu03_RVP = RVP_location_site_by_date(df_RVP_sorted_tempe, 'ASUT03')
df_asu04_RVP = RVP_location_site_by_date(df_RVP_sorted_tempe, 'ASUT04')
df_asu05_RVP = RVP_location_site_by_date(df_RVP_sorted_tempe, 'ASUT05', 'area5')
df_asu06_RVP = RVP_location_site_by_date(df_RVP_sorted_tempe, 'ASUT06', 'area5')
df_asu07_RVP = RVP_location_site_by_date(df_RVP_sorted_tempe, 'ASUT07', 'area2')
df_asu08_RVP = RVP_location_site_by_date(df_RVP_sorted_tempe, 'ASUT08', 'area2')
df_asu09_RVP = RVP_location_site_by_date(df_RVP_sorted_tempe, 'ASUT09', 'area2')
df_asu10_RVP = RVP_location_site_by_date(df_RVP_sorted_tempe, 'ASUT10')
df_asu11_RVP = RVP_location_site_by_date(df_RVP_sorted_tempe, 'ASUT11', 'area1')
df_asu12_RVP = RVP_location_site_by_date(df_RVP_sorted_tempe, 'ASUT12', 'area1')
df_asu14_RVP = RVP_location_site_by_date(df_RVP_sorted_tempe, 'ASUT14', 'area4')
df_asu15_RVP = RVP_location_site_by_date(df_RVP_sorted_tempe, 'ASUT15')
df_asu16_RVP = RVP_location_site_by_date(df_RVP_sorted_tempe, 'ASUT16', 'area4')
df_asu17_RVP = RVP_location_site_by_date(df_RVP_sorted_tempe, 'ASUT17', 'area3')
df_asu19_RVP = RVP_location_site_by_date(df_RVP_sorted_tempe, 'ASUT19')
df_asu20_RVP = RVP_location_site_by_date(df_RVP_sorted_tempe, 'ASUT20', 'area3')
df_asu21_RVP = RVP_location_site_by_date(df_RVP_sorted_tempe, 'ASUT21', 'area3')

# Initializing plotly express graph objects using the dfs above.
p1_RVP = location_date_bar_graph(df_asu01_RVP, 'Date', 'Circulating pathogens', 'ASU Tempe T1', 500, 500)
p2_RVP = location_date_bar_graph(df_asu02_RVP, 'Date', 'Circulating pathogens', 'ASU Tempe T2', 500, 500)
p3_RVP = location_date_bar_graph(df_asu03_RVP, 'Date', 'Circulating pathogens', 'ASU Tempe T3', 500, 500)
p4_RVP = location_date_bar_graph(df_asu04_RVP, 'Date', 'Circulating pathogens', 'ASU Tempe T4', 500, 500)
p5_RVP = location_date_bar_graph(df_asu05_RVP, 'Date', 'Circulating pathogens', 'ASU Tempe T5', 500, 500)
p6_RVP = location_date_bar_graph(df_asu06_RVP, 'Date', 'Circulating pathogens', 'ASU Tempe T6', 500, 500)
p7_RVP = location_date_bar_graph(df_asu07_RVP, 'Date', 'Circulating pathogens', 'ASU Tempe T7', 500, 500)
p8_RVP = location_date_bar_graph(df_asu08_RVP, 'Date', 'Circulating pathogens', 'ASU Tempe T8', 500, 500)
p9_RVP = location_date_bar_graph(df_asu09_RVP, 'Date', 'Circulating pathogens', 'ASU Tempe T9', 500, 500)
p10_RVP = location_date_bar_graph(df_asu10_RVP, 'Date', 'Circulating pathogens', 'ASU Tempe T10', 500, 500)
p11_RVP = location_date_bar_graph(df_asu11_RVP, 'Date', 'Circulating pathogens', 'ASU Tempe T11', 500, 500)
p12_RVP = location_date_bar_graph(df_asu12_RVP, 'Date', 'Circulating pathogens', 'ASU Tempe T12', 500, 500)
p14_RVP = location_date_bar_graph(df_asu14_RVP, 'Date', 'Circulating pathogens', 'ASU Tempe T14', 500, 500)
p15_RVP = location_date_bar_graph(df_asu15_RVP, 'Date', 'Circulating pathogens', 'ASU Tempe T15', 500, 500)
p16_RVP = location_date_bar_graph(df_asu16_RVP, 'Date', 'Circulating pathogens', 'ASU Tempe T16', 500, 500)
p17_RVP = location_date_bar_graph(df_asu17_RVP, 'Date', 'Circulating pathogens', 'ASU Tempe T17', 500, 500)
p19_RVP = location_date_bar_graph(df_asu17_RVP, 'Date', 'Circulating pathogens', 'ASU Tempe T19', 500, 500)
p20_RVP = location_date_bar_graph(df_asu20_RVP, 'Date', 'Circulating pathogens', 'ASU Tempe T20', 500, 500)
p21_RVP = location_date_bar_graph(df_asu21_RVP, 'Date', 'Circulating pathogens', 'ASU Tempe T21', 500, 500)

#_____RVP_read_distribution_____
df_tempe = RVP_split_data_by_campus(RVP_infile, SAMPLE_ID1, SAMPLE_ID2)
df_cumulative_all_Read_Distribution = read_distribution_data_prep(RVP_infile)
df_cumulative_tempe_RD = read_distribution_data_prep(df_tempe)

# Initializing dfs for viral read distributions across all collection locations
df_cumulative_RD_scatter_Adenovirus = read_distribution_scatter_graph(df_cumulative_all_Read_Distribution, 'Adenovirus', 'Historical')
df_cumulative_RD_scatter_Bocavirus = read_distribution_scatter_graph(df_cumulative_all_Read_Distribution, 'Bocavirus', 'Historical')
df_cumulative_RD_scatter_Coronavirus = read_distribution_scatter_graph(df_cumulative_all_Read_Distribution, 'Coronavirus', 'Historical')
df_cumulative_RD_scatter_Enterovirus = read_distribution_scatter_graph(df_cumulative_all_Read_Distribution, 'Enterovirus', 'Historical')
df_cumulative_RD_scatter_Metapneumovirus = read_distribution_scatter_graph(df_cumulative_all_Read_Distribution, 'Metapneumovirus', 'Historical')
df_cumulative_RD_scatter_Parainfluenza = read_distribution_scatter_graph(df_cumulative_all_Read_Distribution, 'Parainfluenza', 'Historical')
df_cumulative_RD_scatter_Parechovirus = read_distribution_scatter_graph(df_cumulative_all_Read_Distribution, 'Parechovirus', 'Historical')
df_cumulative_RD_scatter_RSV = read_distribution_scatter_graph(df_cumulative_all_Read_Distribution, 'RSV', 'Historical')
df_cumulative_RD_scatter_Rhinovirus = read_distribution_scatter_graph(df_cumulative_all_Read_Distribution, 'Rhinovirus', 'Historical')
df_cumulative_RD_scatter_Rubulavirus = read_distribution_scatter_graph(df_cumulative_all_Read_Distribution, 'Rubulavirus', 'Historical')
df_cumulative_RD_scatter_Influenza = read_distribution_scatter_graph(df_cumulative_all_Read_Distribution, 'Influenza', 'Historical')
df_cumulative_RD_scatter_Polyomavirus = read_distribution_scatter_graph(df_cumulative_all_Read_Distribution, 'Polyomavirus', 'Historical')
df_cumulative_RD_scatter_SARS_CoV_2 = read_distribution_scatter_graph(df_cumulative_all_Read_Distribution, 'SARS-CoV-2', 'Historical')

# Initialzing dfs for location specific viral read distributions
df_tempe_RD_scatter_Adenovirus = read_distribution_scatter_graph(df_cumulative_tempe_RD, 'Adenovirus', 'Current')
df_tempe_RD_scatter_Bocavirus = read_distribution_scatter_graph(df_cumulative_tempe_RD, 'Bocavirus', 'Current')
df_tempe_RD_scatter_Coronavirus = read_distribution_scatter_graph(df_cumulative_tempe_RD, 'Coronavirus', 'Current')
df_tempe_RD_scatter_Enterovirus = read_distribution_scatter_graph(df_cumulative_tempe_RD, 'Enterovirus', 'Current')
df_tempe_RD_scatter_Metapneumovirus = read_distribution_scatter_graph(df_cumulative_tempe_RD, 'Metapneumovirus', 'Current')
df_tempe_RD_scatter_Parainfluenza = read_distribution_scatter_graph(df_cumulative_tempe_RD, 'Parainfluenza', 'Current')
df_tempe_RD_scatter_Parechovirus = read_distribution_scatter_graph(df_cumulative_tempe_RD, 'Parechovirus', 'Current')
df_tempe_RD_scatter_RSV = read_distribution_scatter_graph(df_cumulative_tempe_RD, 'RSV', 'Current')
df_tempe_RD_scatter_Rhinovirus = read_distribution_scatter_graph(df_cumulative_tempe_RD, 'Rhinovirus', 'Current')
df_tempe_RD_scatter_Rubulavirus = read_distribution_scatter_graph(df_cumulative_tempe_RD, 'Rubulavirus', 'Current')
df_tempe_RD_scatter_Influenza = read_distribution_scatter_graph(df_cumulative_tempe_RD, 'Influenza', 'Current')
df_tempe_RD_scatter_Polyomavirus = read_distribution_scatter_graph(df_cumulative_tempe_RD, 'Polyomavirus', 'Current')
df_tempe_RD_scatter_SARS_CoV_2 = read_distribution_scatter_graph(df_cumulative_tempe_RD, 'SARS-CoV-2', 'Current')


####_______VSP_ANALYSIS_________####
VSP_infile = pd.read_csv(f'data/wastewater_virus_surveillance/combined/VSP_grouped_counts.csv')
VSP_infile = VSP_infile.rename(columns={'Unnamed: 0': 'Seq_ID'})

# preparing VSP location dfs
# VSP_infile = sort_df_data(VSP_infile).reset_index()
df_tempe_VSP = VSP_infile[VSP_infile['Site'].str.startswith(LOCATION_ID)]

# group grouped VSP viruses by date.
df_tempe_VSP = df_tempe_VSP.drop(columns=['Seq_ID', 'Site', 'External_ID']).groupby('Date').sum().reset_index()
df_tempe_VSP = sort_df_data(df_tempe_VSP)


#___formatting___
st.sidebar.header('ASU Tempe Wastewater Virus Tracker')
st.markdown('# ASU Tempe Campus Wastewater Virus Tracker')
st.markdown(f"#### Today's Date: {date1}")
st.markdown(f'#### Last Updated: {ww_update_date}')
st.markdown('---')
st.write(
    '''
    ### About this page
    This page displays SARS-CoV-2 and Respiratory Virus Pannel(RVP) Next Generation Sequencing(NGS) data generated from samples collected across ASU Tempe campus.

    The various charts on this page are interactive with features including zooming, panning, and exporting as png files.

    The data displayed represent a shifting 15 week window based on wastewater sample collection dates.
    '''
)
st.markdown('---')
st.markdown(f'### Tempe Collection Locations')

col_a1, col_a2 = st.columns([3, 1])
with col_a1:
    st_data = st_folium(m, height=600, width=1200)
with col_a2:
    st.dataframe(df_location, height=600, width=400)

# If streamlit-foium map goes down/buggs out, uncommnet line below then comment out line 274 (Display error message) and lines 266-270 (Map and table visualization). Repeat for other pages.
# st.markdown('The interactive map has been disabled for the time being due to incompatibilites with the Streamlit app that arose due to new version update.')
st.markdown('The map and table above displays Tempe campus sample collection locations and their corresponding IDs, and facilities.')
st.markdown('---')

col_b1, col_b2 = st.columns([1, 1])
#__Freyja_graphs__
with col_b1:
    st.markdown('### Relative abundance of SARS-CoV-2 Variants')
    tab1, tab2, tab3, tab4, tab5, \
        tab6, tab7, tab8, tab9, tab10, \
        tab11, tab12, tab14, tab15, tab16,\
        tab17, tab18, tab19, tab20, tab21 = st.tabs(['T1', 'T2', 'T3', 'T4', 'T5',
                                                     'T6', 'T7', 'T8', 'T9', 'T10',
                                                     'T11', 'T12', 'T14', 'T15', 'T16',
                                                     'T17', 'T18', 'T19', 'T20', 'T21'])
    with tab1:
        st.plotly_chart(p1_freyja)
    with tab2:
        st.plotly_chart(p2_freyja)
    with tab3:
        st.plotly_chart(p3_freyja)
    with tab4:
        st.plotly_chart(p4_freyja)
    with tab5:
        st.plotly_chart(p5_freyja)
    with tab6:
        st.plotly_chart(p6_freyja)
    with tab7:
        st.plotly_chart(p7_freyja)
    with tab8:
        st.plotly_chart(p8_freyja)
    with tab9:
        st.plotly_chart(p9_freyja)
    with tab10:
        st.plotly_chart(p10_freyja)
    with tab11:
        st.plotly_chart(p11_freyja)
    with tab12:
        st.plotly_chart(p12_freyja)
    with tab14:
        st.plotly_chart(p14_freyja)
    with tab15:
        st.plotly_chart(p15_freyja)
    with tab16:
        st.plotly_chart(p16_freyja)
    with tab17:
        st.plotly_chart(p17_freyja)
    with tab18:
        st.plotly_chart(p18_freyja)
    with tab19:
        st.plotly_chart(p17_freyja)
    with tab20:
        st.plotly_chart(p20_freyja)
    with tab21:
        st.plotly_chart(p21_freyja)
    st.markdown('The figure above displays relative abundance data for SARS-CoV-2 lineages for the most recent 5 week window.  \n \
                 Deselecting a lineage from the legend will hide it from the chart.')

with col_b2:
    #___RVP_graphs___
    st.markdown('### Relative abundance of Pathogens')
    tab1, tab2, tab3, tab4, tab5, \
        tab6, tab7, tab8, tab9, tab10, \
        tab11, tab12, tab14, tab15, tab16,\
        tab17, tab19, tab20, tab21 = st.tabs(['T1', 'T2', 'T3', 'T4', 'T5',
                                              'T6', 'T7', 'T8', 'T9', 'T10',
                                              'T11', 'T12', 'T14', 'T15', 'T16',
                                              'T17', 'T19', 'T20', 'T21'])
    with tab1:
        st.plotly_chart(p1_RVP)
    with tab2:
        st.plotly_chart(p2_RVP)
    with tab3:
        st.plotly_chart(p3_RVP)
    with tab4:
        st.plotly_chart(p4_RVP)
    with tab5:
        st.plotly_chart(p5_RVP)
    with tab6:
        st.plotly_chart(p6_RVP)
    with tab7:
        st.plotly_chart(p7_RVP)
    with tab8:
        st.plotly_chart(p8_RVP)
    with tab9:
        st.plotly_chart(p9_RVP)
    with tab10:
        st.plotly_chart(p10_RVP)
    with tab11:
        st.plotly_chart(p11_RVP)
    with tab12:
        st.plotly_chart(p12_RVP)
    with tab14:
        st.plotly_chart(p14_RVP)
    with tab15:
        st.plotly_chart(p15_RVP)
    with tab16:
        st.plotly_chart(p16_RVP)
    with tab17:
        st.plotly_chart(p17_RVP)
    with tab19:
        st.plotly_chart(p19_RVP)
    with tab20:
        st.plotly_chart(p20_RVP)
    with tab21:
        st.plotly_chart(p21_RVP)
    st.markdown('The figure above displays relative abundance data for RVP pathogens for the most recent 5 week window.  \n \
                 Deselecting a pathogen from the legend will hide it from the chart.')

st.markdown('---')
st.markdown('### Relative Abundance Charts')
tab1, tab2, tab3 = st.tabs(['SARS-CoV-2 variants (Bar)', 'Respiratory Pathogen Averaged Mapped Counts (Line)', 'Viral Surveillance Pannel Total Mapped Counts (Line)'])
with tab1:
    st.plotly_chart(p_freyja_date, height=500, use_container_width=True)
    st.markdown('The figure above displays the relative abundance of currently circulating SARS-CoV-2 variants by sampling date. Abundance values are an aggregate of Freyja analysis variant calling using iVar.')
with tab2:
    st.plotly_chart(RVP_avg_count_lines(RVP_infile2[-16:], False), height=500, use_container_width=True)
    st.markdown('The figure above displays the average mapped reads of currently circulating viruses by collection date. Averages were determined using total reads mapped to each pathogen  \n \
                 for the given collection week divided by the total number of collection sites for that week.')
with tab3:
    st.plotly_chart(VSP_counts_line_graph(df_tempe_VSP, 'Tempe'), use_container_width=True)
    st.markdown('The graph above displays the total mapped reads for grouped VSP viruses by collection date.')

st.markdown('---')
st.markdown('### Viral Read Distributions at a Glance')
# Weekly Read Distribution table
st.dataframe(df_tempe_reads[::-1].style.apply(HIGHLIGHTER, axis=0), height=248, use_container_width=True)
st.markdown(f'The table above displays the weekly maximum mapped read count for each circulating pathogen. Cell colors (:red[High], :orange[Medium], :green[Low]) reflect weekly count in relation to historical trends.')
st.markdown('---')

#_____read_distribution_data______
tab1, tab2, tab3, tab4, tab5, \
    tab6, tab7, tab8, tab9, tab10, \
    tab11, tab12, tab13 = st.tabs(['Adenovirus', 'Bocavirus', 'Coronavirus', 'Enterovirus', 'Metapneumovirus',
                                   'Parainfluenza', 'Parechovirus', 'RSV', 'Rhinovirus', 'Rubulavirus',
                                   'Influenza', 'Polyomavirus', 'SARS-CoV-2'])
with tab1:
    col_c1, col_c2, = st.columns(2)
    with col_c1:
        st.plotly_chart(df_cumulative_RD_scatter_Adenovirus)
    with col_c2:
        st.plotly_chart(df_tempe_RD_scatter_Adenovirus)
with tab2:
    col_c1, col_c2, = st.columns(2)
    with col_c1:
        st.plotly_chart(df_cumulative_RD_scatter_Bocavirus)
    with col_c2:
        st.plotly_chart(df_tempe_RD_scatter_Bocavirus)
with tab3:
    col_c1, col_c2, = st.columns(2)
    with col_c1:
        st.plotly_chart(df_cumulative_RD_scatter_Coronavirus)
    with col_c2:
        st.plotly_chart(df_tempe_RD_scatter_Coronavirus)
with tab4:
    col_c1, col_c2, = st.columns(2)
    with col_c1:
        st.plotly_chart(df_cumulative_RD_scatter_Enterovirus)
    with col_c2:
        st.plotly_chart(df_tempe_RD_scatter_Enterovirus)
with tab5:
    col_c1, col_c2, = st.columns(2)
    with col_c1:
        st.plotly_chart(df_cumulative_RD_scatter_Metapneumovirus)
    with col_c2:
        st.plotly_chart(df_tempe_RD_scatter_Metapneumovirus)
with tab6:
    col_c1, col_c2, = st.columns(2)
    with col_c1:
        st.plotly_chart(df_cumulative_RD_scatter_Parainfluenza)
    with col_c2:
        st.plotly_chart(df_tempe_RD_scatter_Parainfluenza)
with tab7:
    col_c1, col_c2, = st.columns(2)
    with col_c1:
        st.plotly_chart(df_cumulative_RD_scatter_Parechovirus)
    with col_c2:
        st.plotly_chart(df_tempe_RD_scatter_Parechovirus)
with tab8:
    col_c1, col_c2, = st.columns(2)
    with col_c1:
        st.plotly_chart(df_cumulative_RD_scatter_RSV)
    with col_c2:
        st.plotly_chart(df_tempe_RD_scatter_RSV)
with tab9:
    col_c1, col_c2, = st.columns(2)
    with col_c1:
        st.plotly_chart(df_cumulative_RD_scatter_Rhinovirus)
    with col_c2:
        st.plotly_chart(df_tempe_RD_scatter_Rhinovirus)
with tab10:
    col_c1, col_c2, = st.columns(2)
    with col_c1:
        st.plotly_chart(df_cumulative_RD_scatter_Rubulavirus)
    with col_c2:
        st.plotly_chart(df_tempe_RD_scatter_Rubulavirus)
with tab11:
    col_c1, col_c2, = st.columns(2)
    with col_c1:
        st.plotly_chart(df_cumulative_RD_scatter_Influenza)
    with col_c2:
        st.plotly_chart(df_tempe_RD_scatter_Influenza)
with tab12:
    col_c1, col_c2, = st.columns(2)
    with col_c1:
        st.plotly_chart(df_cumulative_RD_scatter_Polyomavirus)
    with col_c2:
        st.plotly_chart(df_tempe_RD_scatter_Polyomavirus)
with tab13:
    col_c1, col_c2, = st.columns(2)
    with col_c1:
        st.plotly_chart(df_cumulative_RD_scatter_SARS_CoV_2)
    with col_c2:
        st.plotly_chart(df_tempe_RD_scatter_SARS_CoV_2)

st.markdown('The figures above displays historic trends in confirmed viral reads arranged in ascending order by sample across all campuses. The figure to the right displays the range of reads for ASU Tempe campus.  \n \
             Comparison of the two figures allows for quick insights regarding current pathogen prevelence levels.')
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
