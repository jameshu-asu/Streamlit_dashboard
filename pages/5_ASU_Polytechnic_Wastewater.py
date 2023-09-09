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
# This page displays ASU Polytechnic campus wastewater data.


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
    page_title='Polytechnic Campus',
    page_icon='🚱',
    layout='wide'
)

####_______FOLIUM_MAP_________####

# latitude and longitudes positions correspond with popups and tooltips in the same index position
latitudes_list = [33.339472, 33.339474, 33.337635, 33.337655, 33.337718,
                  33.337738, 33.336597, 33.336474]

longitudes_list = [-111.677550, -111.676791, -111.675040, -111.675590, -111.676987,
                   -111.677566, -111.676340, -111.679266]

popups = ['ASU Polytechnic: P1', 'ASU Polytechnic: P2', 'ASU Polytechnic: P3', 'ASU Polytechnic: P4', 'ASU Polytechnic: P5',
          'ASU Polytechnic: P6', 'ASU Polytechnic: P7', 'ASU Polytechnic: P8']

tooltips = ['P1', 'P2', 'P3', 'P4', 'P5',
            'P6', 'P7', 'P8']

# Center at latitude/longitude coordinates.
m = folium.Map(location=[33.338398, -111.676245], zoom_start=17)

# Add markers
for i, j, k, l in zip(latitudes_list, longitudes_list, popups, tooltips):
    iframe = folium.IFrame(k)
    folium.Marker(
        location=[i, j],
        popup=folium.Popup(iframe, min_width=275, max_width=275, min_height=50, max_height=50),
        tooltip=l,
        icon=folium.Icon(color='blue')

    ).add_to(m)

####_______FREYJA_ANALYSIS_________####
Freyja_infile = pd.read_csv('data/wastewater_virus_surveillance/combined/Combined_freyja_grouped_metadata_analysis.csv')

# set location for location codes and location specific read disttribution data.
LOCATION: Final = 'polytechnic'
LOCATION_ID: Final = 'ASUP'
SAMPLE_ID: Final = 'AWMP'

# reads from combined_freyja metadata file, sorts by campus location
# location_code polytechnic: ASUT, Polytechnic: ASUP, West: ASUW, Downtown: ASUDT
df_freyja_sorted_polytechnic = freyja_sort_by_location(Freyja_infile, LOCATION_ID)
df_freyja_date = freyja_by_date(df_freyja_sorted_polytechnic)
# resetting index because merge function sets df index to "Date" and sort_df_date function needs "Date" to be in a column
df_freyja_date = df_freyja_date.reset_index()
df_freyja_date = sort_df_data(df_freyja_date).tail(16)

df_location = locations(LOCATION)
df_polytechnic_reads = read_distribution(LOCATION).tail(6)

#____Freyja_averaged_charts_____
df_melt1 = organize_df(df_freyja_date, 'Date')
# df_melt2 = organize_df(df_freyja_site, 'Site')
p_freyja_date = location_date_bar_graph(df_melt1, 'Date', 'Variant', 'ASU Polytechnic Wastewater SARS-CoV-2 Variants', 500, 500)
# p_freyja_site = location_date_bar_graph(df_melt2, 'Site', 'ASU polytechnic Wastewater SARS-CoV-2 Variants by Location')

#____Freyja_site_specific_charts____
df_site_date_freyja = freyja_sort_by_location(Freyja_infile, LOCATION_ID, 'area7', 'area6')

# Initializing dfs for collection site specific SARS-CoV-2 variant abundance by colletion date data.
df_asu01_freyja = freyja_location_site_by_date(df_site_date_freyja, 'ASUP01')
df_asu02_freyja = freyja_location_site_by_date(df_site_date_freyja, 'ASUP02')
df_asu03_freyja = freyja_location_site_by_date(df_site_date_freyja, 'ASUP03', 'area6')
df_asu04_freyja = freyja_location_site_by_date(df_site_date_freyja, 'ASUP04', 'area6')
df_asu05_freyja = freyja_location_site_by_date(df_site_date_freyja, 'ASUP05', 'area7')
df_asu06_freyja = freyja_location_site_by_date(df_site_date_freyja, 'ASUP06', 'area7')
df_asu07_freyja = freyja_location_site_by_date(df_site_date_freyja, 'ASUP07')
df_asu08_freyja = freyja_location_site_by_date(df_site_date_freyja, 'ASUP08')


# Initializing plotly express graph objects using the dfs above.
p1_freyja = location_date_bar_graph(df_asu01_freyja, 'Date', 'Variants', 'ASU Polytechnic P1', 500, 500)
p2_freyja = location_date_bar_graph(df_asu02_freyja, 'Date', 'Variants', 'ASU Polytechnic P2', 500, 500)
p3_freyja = location_date_bar_graph(df_asu03_freyja, 'Date', 'Variants', 'ASU Polytechnic P3', 500, 500)
p4_freyja = location_date_bar_graph(df_asu04_freyja, 'Date', 'Variants', 'ASU Polytechnic P4', 500, 500)
p5_freyja = location_date_bar_graph(df_asu05_freyja, 'Date', 'Variants', 'ASU Polytechnic P5', 500, 500)
p6_freyja = location_date_bar_graph(df_asu06_freyja, 'Date', 'Variants', 'ASU Polytechnic P6', 500, 500)
p7_freyja = location_date_bar_graph(df_asu07_freyja, 'Date', 'Variants', 'ASU Polytechnic P7', 500, 500)
p8_freyja = location_date_bar_graph(df_asu08_freyja, 'Date', 'Variants', 'ASU Polytechnic P8', 500, 500)


####_______RVP_ANALYSIS_________####
RVP_infile = pd.read_csv(f'data/wastewater_virus_surveillance/combined/RVP_counts_virusOnly_normalized_filled_{run}.csv')
RVP_infile2 = pd.read_csv(f'data/wastewater_virus_surveillance/polytechnic/rvp/RVP_counts_polytechnic_normalized_avg_groupby_date.csv', index_col=0)

#____RVP_site_specific_charts___
df_RVP_sorted_polytechnic = RVP_sort_by_location(RVP_infile, LOCATION_ID)

# Initializing dfs for collection site specific SARS-CoV-2 variant abundance by colletion date data.
df_asu01_RVP = RVP_location_site_by_date(df_RVP_sorted_polytechnic, 'ASUP01')
df_asu02_RVP = RVP_location_site_by_date(df_RVP_sorted_polytechnic, 'ASUP02')
df_asu03_RVP = RVP_location_site_by_date(df_RVP_sorted_polytechnic, 'ASUP03', 'area6_area')
df_asu04_RVP = RVP_location_site_by_date(df_RVP_sorted_polytechnic, 'ASUP04', 'area6_area')
df_asu05_RVP = RVP_location_site_by_date(df_RVP_sorted_polytechnic, 'ASUP05', 'area7_area')
df_asu06_RVP = RVP_location_site_by_date(df_RVP_sorted_polytechnic, 'ASUP06', 'area7_area')
df_asu07_RVP = RVP_location_site_by_date(df_RVP_sorted_polytechnic, 'ASUP07')
df_asu08_RVP = RVP_location_site_by_date(df_RVP_sorted_polytechnic, 'ASUP08')


# Initializing plotly express graph objects using the dfs above.
p1_RVP = location_date_bar_graph(df_asu01_RVP, 'Date', 'Circulating pathogens', 'ASU Polytechnic P1', 500, 500)
p2_RVP = location_date_bar_graph(df_asu02_RVP, 'Date', 'Circulating pathogens', 'ASU Polytechnic P2', 500, 500)
p3_RVP = location_date_bar_graph(df_asu03_RVP, 'Date', 'Circulating pathogens', 'ASU Polytechnic P3', 500, 500)
p4_RVP = location_date_bar_graph(df_asu04_RVP, 'Date', 'Circulating pathogens', 'ASU Polytechnic P4', 500, 500)
p5_RVP = location_date_bar_graph(df_asu05_RVP, 'Date', 'Circulating pathogens', 'ASU Polytechnic P5', 500, 500)
p6_RVP = location_date_bar_graph(df_asu06_RVP, 'Date', 'Circulating pathogens', 'ASU Polytechnic P6', 500, 500)
p7_RVP = location_date_bar_graph(df_asu07_RVP, 'Date', 'Circulating pathogens', 'ASU Polytechnic P7', 500, 500)
p8_RVP = location_date_bar_graph(df_asu08_RVP, 'Date', 'Circulating pathogens', 'ASU Polytechnic P8', 500, 500)


#_____RVP_read_distribution_____
df_polytechnic = RVP_split_data_by_campus(RVP_infile, SAMPLE_ID)
df_cumulative_all_Read_Distribution = read_distribution_data_prep(RVP_infile)
df_cumulative_polytechnic_RD = read_distribution_data_prep(df_polytechnic)

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
df_polytechnic_RD_scatter_Adenovirus = read_distribution_scatter_graph(df_cumulative_polytechnic_RD, 'Adenovirus', 'Current')
df_polytechnic_RD_scatter_Bocavirus = read_distribution_scatter_graph(df_cumulative_polytechnic_RD, 'Bocavirus', 'Current')
df_polytechnic_RD_scatter_Coronavirus = read_distribution_scatter_graph(df_cumulative_polytechnic_RD, 'Coronavirus', 'Current')
df_polytechnic_RD_scatter_Enterovirus = read_distribution_scatter_graph(df_cumulative_polytechnic_RD, 'Enterovirus', 'Current')
df_polytechnic_RD_scatter_Metapneumovirus = read_distribution_scatter_graph(df_cumulative_polytechnic_RD, 'Metapneumovirus', 'Current')
df_polytechnic_RD_scatter_Parainfluenza = read_distribution_scatter_graph(df_cumulative_polytechnic_RD, 'Parainfluenza', 'Current')
df_polytechnic_RD_scatter_Parechovirus = read_distribution_scatter_graph(df_cumulative_polytechnic_RD, 'Parechovirus', 'Current')
df_polytechnic_RD_scatter_RSV = read_distribution_scatter_graph(df_cumulative_polytechnic_RD, 'RSV', 'Current')
df_polytechnic_RD_scatter_Rhinovirus = read_distribution_scatter_graph(df_cumulative_polytechnic_RD, 'Rhinovirus', 'Current')
df_polytechnic_RD_scatter_Rubulavirus = read_distribution_scatter_graph(df_cumulative_polytechnic_RD, 'Rubulavirus', 'Current')
df_polytechnic_RD_scatter_Influenza = read_distribution_scatter_graph(df_cumulative_polytechnic_RD, 'Influenza', 'Current')
df_polytechnic_RD_scatter_Polyomavirus = read_distribution_scatter_graph(df_cumulative_polytechnic_RD, 'Polyomavirus', 'Current')
df_polytechnic_RD_scatter_SARS_CoV_2 = read_distribution_scatter_graph(df_cumulative_polytechnic_RD, 'SARS-CoV-2', 'Current')

####_______VSP_ANALYSIS_________####
VSP_infile = pd.read_csv(f'data/wastewater_virus_surveillance/combined/VSP_grouped_counts.csv')
VSP_infile = VSP_infile.rename(columns={'Unnamed: 0': 'Seq_ID'})

# preparing VSP location dfs
# VSP_infile = sort_df_data(VSP_infile).reset_index()
df_polytechnic_VSP = VSP_infile[VSP_infile['Site'].str.startswith(LOCATION_ID)]

# group grouped VSP viruses by date.
df_polytechnic_VSP = df_polytechnic_VSP.drop(columns=['Seq_ID', 'Site', 'External_ID']).groupby('Date').sum().reset_index()
df_polytechnic_VSP = sort_df_data(df_polytechnic_VSP)


#___formatting___
st.sidebar.header('ASU Polytechnic Wastewater Virus Tracker')
st.markdown('# ASU Polytechnic Campus Wastewater Virus Tracker')
st.markdown(f"#### Today's Date: {date1}")
st.markdown(f'#### Last Updated: {ww_update_date}')
st.markdown('---')
st.write(
    '''
    ### About this page
    This page displays SARS-CoV-2 and Respiratory Virus Pannel(RVP) Next Generation Sequencing(NGS) data generated from samples collected across ASU Polytechnic campus.

    The various charts on this page are interactive with features including zooming, panning, and exporting as png files.

    The data displayed represent a shifting 15 week window based on wastewater sample collection dates.
    '''
)
st.markdown('---')
st.write('### Polytechnic Collection Locations')

col_a1, col_a2 = st.columns([3, 1])
with col_a1:
    st_data = st_folium(m, height=600, width=1000)
with col_a2:
    st.dataframe(df_location, height=600, width=400)

# If streamlit-foium map goes down/buggs out, uncommnet line below then comment out line 219 (Display error message) and lines 211-215 (Map and table visualization). Repeat for other pages.
# st.markdown('The interactive map has been disabled for the time being due to incompatibilites with the Streamlit app that arose due to new version update.')
st.markdown('The map and table above displays Polytechnic campus sample collection locations and their corresponding IDs, and facilities.')
st.markdown('---')

col_b1, col_b2 = st.columns([1, 1])
#__Freyja_graphs__
with col_b1:
    st.markdown('### Relative abundance of SARS-CoV-2 Variants')
    tab1, tab2, tab3, tab4, tab5, \
        tab6, tab7, tab8 = st.tabs(['P1', 'P2', 'P3', 'P4', 'P5',
                                    'P6', 'P7', 'P8'])
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
    st.markdown('The figure above displays relative abundance data for SARS-CoV-2 lineages for the most recent 5 week window.  \n \
                 Deselecting a lineage from the legend will hide it from the chart.')


with col_b2:
    #___RVP_graphs___
    st.markdown('### Relative abundance of Pathogens')
    tab1, tab2, tab3, tab4, tab5, \
        tab6, tab7, tab8 = st.tabs(['P1', 'P2', 'P3', 'P4', 'P5',
                                    'P6', 'P7', 'P8'])
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
    st.markdown('The figure above displays relative abundance data for RVP pathogens for the most recent 5 week window.  \n\
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
    st.plotly_chart(VSP_counts_line_graph(df_polytechnic_VSP, 'polytechnic'), use_container_width=True)
    st.markdown('The graph above displays the total mapped reads for grouped VSP viruses by collection date.')

st.markdown('---')
st.markdown('### Viral Read Distributions at a Glance')

# Weekly Read Distribution table
st.dataframe(df_polytechnic_reads[::-1].style.apply(HIGHLIGHTER, axis=0), height=248, use_container_width=True)
st.markdown(f'The table above displays the weekly maximum mapped read count for circulating pathogens.\
            Cell colors (:red[High], :orange[Medium], :green[Low]) reflect weekly count in relation to historical trends.')
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
        st.plotly_chart(df_polytechnic_RD_scatter_Adenovirus)
with tab2:
    col_c1, col_c2, = st.columns(2)
    with col_c1:
        st.plotly_chart(df_cumulative_RD_scatter_Bocavirus)
    with col_c2:
        st.plotly_chart(df_polytechnic_RD_scatter_Bocavirus)
with tab3:
    col_c1, col_c2, = st.columns(2)
    with col_c1:
        st.plotly_chart(df_cumulative_RD_scatter_Coronavirus)
    with col_c2:
        st.plotly_chart(df_polytechnic_RD_scatter_Coronavirus)
with tab4:
    col_c1, col_c2, = st.columns(2)
    with col_c1:
        st.plotly_chart(df_cumulative_RD_scatter_Enterovirus)
    with col_c2:
        st.plotly_chart(df_polytechnic_RD_scatter_Enterovirus)
with tab5:
    col_c1, col_c2, = st.columns(2)
    with col_c1:
        st.plotly_chart(df_cumulative_RD_scatter_Metapneumovirus)
    with col_c2:
        st.plotly_chart(df_polytechnic_RD_scatter_Metapneumovirus)
with tab6:
    col_c1, col_c2, = st.columns(2)
    with col_c1:
        st.plotly_chart(df_cumulative_RD_scatter_Parainfluenza)
    with col_c2:
        st.plotly_chart(df_polytechnic_RD_scatter_Parainfluenza)
with tab7:
    col_c1, col_c2, = st.columns(2)
    with col_c1:
        st.plotly_chart(df_cumulative_RD_scatter_Parechovirus)
    with col_c2:
        st.plotly_chart(df_polytechnic_RD_scatter_Parechovirus)
with tab8:
    col_c1, col_c2, = st.columns(2)
    with col_c1:
        st.plotly_chart(df_cumulative_RD_scatter_RSV)
    with col_c2:
        st.plotly_chart(df_polytechnic_RD_scatter_RSV)
with tab9:
    col_c1, col_c2, = st.columns(2)
    with col_c1:
        st.plotly_chart(df_cumulative_RD_scatter_Rhinovirus)
    with col_c2:
        st.plotly_chart(df_polytechnic_RD_scatter_Rhinovirus)
with tab10:
    col_c1, col_c2, = st.columns(2)
    with col_c1:
        st.plotly_chart(df_cumulative_RD_scatter_Rubulavirus)
    with col_c2:
        st.plotly_chart(df_polytechnic_RD_scatter_Rubulavirus)
with tab11:
    col_c1, col_c2, = st.columns(2)
    with col_c1:
        st.plotly_chart(df_cumulative_RD_scatter_Influenza)
    with col_c2:
        st.plotly_chart(df_polytechnic_RD_scatter_Influenza)
with tab12:
    col_c1, col_c2, = st.columns(2)
    with col_c1:
        st.plotly_chart(df_cumulative_RD_scatter_Polyomavirus)
    with col_c2:
        st.plotly_chart(df_polytechnic_RD_scatter_Polyomavirus)
with tab13:
    col_c1, col_c2, = st.columns(2)
    with col_c1:
        st.plotly_chart(df_cumulative_RD_scatter_SARS_CoV_2)
    with col_c2:
        st.plotly_chart(df_polytechnic_RD_scatter_SARS_CoV_2)

st.markdown('The figures above displays historic trends in confirmed viral reads arranged in ascending order by sample across all campuses. The figure to the right displays the range of reads for ASU Polytechnic campus.  \n \
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
