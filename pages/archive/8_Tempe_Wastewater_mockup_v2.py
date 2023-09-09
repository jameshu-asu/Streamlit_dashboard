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

st.set_page_config(
    page_title='Tempe Campus',
    page_icon='🚱',
    layout='wide'
)

####_______FOLIUM_MAP_________####

# latitude and longitudes positions correspond with popups and tooltips in the same index position
latitudes_list = [33.422039, 33.423573, 33.418049, 33.422113, 33.423294,
                  33.422863, 33.416281, 33.415880, 33.415257, 33.414915,
                  33.412871, 33.412884, 33.416039, 33.414170, 33.415984,
                  33.419664]

longitudes_list = [-111.933943, -111.933783, -111.926203, -111.930186, -111.933761,
                   -111.933746, -111.929055, -111.930002, -111.930380, -111.928599,
                   -111.927151, -111.927948, -111.935788, -111.931554, -111.932021,
                   -111.935681]

popups = ['ASU Tempe: T1(Palo Verde)', 'ASU Tempe: T2(Tooker C)', 'ASU Tempe: T3(Greek)', 'ASU Tempe: T4(Manzanita)', 'ASU Tempe: T5(Tooker A)',
          'ASU Tempe: T6(Palo Verde)', 'ASU Tempe T7: (Hassayampa A)', 'ASU Tempe T8: (Hassayampa B)', 'ASU Tempe T9: (Hassayampa C)', 'ASU Tempe T10: (Barrett College)',
          'ASU Tempe: T11 (Adelphi East)', 'ASU Tempe: T12 (Adelphi Commons)', 'ASU Tempe: T14 (Best)', 'ASU Tempe: T15 (Villas at Vista)', 'ASU Tempe: T16 (Gym)',
          'ASU Tempe: T17 (Hayden Library)', 'ASU Tempe: T20 (MU)', 'ASU Tempe: T21 (Student Pavilion)']

tooltips = ['T1', 'T2', 'T3', 'T4', 'T5',
            'T6', 'T7', 'T8', 'T9', 'T10',
            'T11', 'T12', 'T14', 'T15', 'T16',
            'T17', 'T20', 'T21']

# Center at latitude/longitude coordinates.
m = folium.Map(location=[33.418298, -111.932704], zoom_start=15)

# Add markers iteratively using the zipped lists.
for i, j, k, l in zip(latitudes_list, longitudes_list, popups, tooltips):
    folium.Marker(
                location=[i, j],
                popup=k,
                tooltip=l,
                icon=folium.Icon(color='orange')

    ).add_to(m)


####_______FREYJA_ANALYSIS_________####

# set location for location codes and location specific read disttribution data.
location = 'tempe'

# reads from combined_freyja metadata file, sorts by campus location
# location_code Tempe: ASUT, Polytechnic: ASUP, West: ASUW, Downtown: ASUDT
df_freyja_sorted_tempe = freyja_sort_by_location('ASUT')
df_freyja_date = freyja_by_date(df_freyja_sorted_tempe)
# resetting index because merge function sets df index to "Date" and sort_df_date function needs "Date" to be in a column
df_freyja_date = df_freyja_date.reset_index()
df_freyja_date = sort_df_data(df_freyja_date)

df_location = locations(location)
df_tempe_reads = read_distribution(location)

#____Freyja_averaged_charts_____
df_melt1 = organize_df(df_freyja_date, 'Date')
# df_melt2 = organize_df(df_freyja_site, 'Site')
p_freyja_date = location_date_bar_graph(df_melt1, 'Date', 'ASU Tempe Wastewater SARS-CoV-2 Variants by Date')
# p_freyja_site = location_date_bar_graph(df_melt2, 'Site', 'ASU Tempe Wastewater SARS-CoV-2 Variants by Location')

#____Freyja_site_specific_charts____
df_site_date_freyja = freyja_by_site_date(df_freyja_sorted_tempe)

# Initializing dfs for collection site specific SARS-CoV-2 variant abundance by colletion date data.
df_asu01_freyja = location_site_date(df_site_date_freyja, 'ASUT01')
df_asu02_freyja = location_site_date(df_site_date_freyja, 'ASUT02')
df_asu03_freyja = location_site_date(df_site_date_freyja, 'ASUT03')
df_asu04_freyja = location_site_date(df_site_date_freyja, 'ASUT04')
df_asu05_freyja = location_site_date(df_site_date_freyja, 'ASUT05')
df_asu06_freyja = location_site_date(df_site_date_freyja, 'ASUT06')
df_asu07_freyja = location_site_date(df_site_date_freyja, 'ASUT07')
df_asu08_freyja = location_site_date(df_site_date_freyja, 'ASUT08')
df_asu09_freyja = location_site_date(df_site_date_freyja, 'ASUT09')
df_asu10_freyja = location_site_date(df_site_date_freyja, 'ASUT10')
df_asu11_freyja = location_site_date(df_site_date_freyja, 'ASUT11')
df_asu12_freyja = location_site_date(df_site_date_freyja, 'ASUT12')
df_asu14_freyja = location_site_date(df_site_date_freyja, 'ASUT14')
df_asu15_freyja = location_site_date(df_site_date_freyja, 'ASUT15')
df_asu16_freyja = location_site_date(df_site_date_freyja, 'ASUT16')
df_asu17_freyja = location_site_date(df_site_date_freyja, 'ASUT17')
df_asu20_freyja = location_site_date(df_site_date_freyja, 'ASUT20')
df_asu21_freyja = location_site_date(df_site_date_freyja, 'ASUT21')

# Initializing plotly express graph objects using the dfs above.
p1_freyja = site_date_bar_graph(df_asu01_freyja.tail(5), 'ASU Tempe T1 (Palo Verde)')
p2_freyja = site_date_bar_graph(df_asu02_freyja.tail(5), 'ASU Tempe T2 (Tooker C)')
p3_freyja = site_date_bar_graph(df_asu03_freyja.tail(5), 'ASU Tempe T3 (Greek)')
p4_freyja = site_date_bar_graph(df_asu04_freyja.tail(5), 'ASU Tempe T4 (Manzanita)')
p5_freyja = site_date_bar_graph(df_asu05_freyja.tail(5), 'ASU Tempe T5 (Tooker A)')
p6_freyja= site_date_bar_graph(df_asu06_freyja.tail(5), 'ASU Tempe T6 (Tooker B)')
p7_freyja = site_date_bar_graph(df_asu07_freyja.tail(5), 'ASU Tempe T7 (Hassayampa A)')
p8_freyja = site_date_bar_graph(df_asu08_freyja.tail(5), 'ASU Tempe T8 (Hassayampa B)')
p9_freyja = site_date_bar_graph(df_asu09_freyja.tail(5), 'ASU Tempe T9 (Hassayampa C)')
p10_freyja = site_date_bar_graph(df_asu10_freyja.tail(5), 'ASU Tempe T10 (Barrett College)')
p11_freyja = site_date_bar_graph(df_asu11_freyja.tail(5), 'ASU Tempe T11 (Adelphi East)')
p12_freyja = site_date_bar_graph(df_asu12_freyja.tail(5), 'ASU Tempe T12 (Adelphi Commons)')
p14_freyja = site_date_bar_graph(df_asu14_freyja.tail(5), 'ASU Tempe T14 (Best)')
p15_freyja = site_date_bar_graph(df_asu15_freyja.tail(5), 'ASU Tempe T15 (Villas at Vista)')
p16_freyja = site_date_bar_graph(df_asu16_freyja.tail(5), 'ASU Tempe T16 (Gym)')
p17_freyja = site_date_bar_graph(df_asu17_freyja.tail(5), 'ASU Tempe T17 (Hayden Library)')
p20_freyja = site_date_bar_graph(df_asu20_freyja.tail(5), 'ASU Tempe T20 (MU)')
p21_freyja = site_date_bar_graph(df_asu21_freyja.tail(5), 'ASU Tempe T21 (Student Pavilion)')


####_______RVP_ANALYSIS_________####

#____RVP_averaged_graph_____
df_tempe_data = sort_csv_data(f'data/dataframes/weekly_counts_avg_345.csv').tail(15).copy()
df_tempe_data = df_tempe_data.reset_index()
date_list = [i.strftime('%b-%d-%Y') for i in df_tempe_data['Date']]
df_tempe_data['Date'] = date_list
df_tempe_data = df_tempe_data.set_index('Date')
df_tempe_data1 = df_tempe_data.T.copy()
df_tempe_data1 = organize_df_by_virus(df_tempe_data1)
p_ww_stacked_bar_current = stacked_bar_graph(df_tempe_data1)

#____RVP_site_specific_charts____


df_rvp_sorted_tempe = RVP_sort_by_location('ASUT')
df_site_date_RVP = RVP_by_site_date(df_rvp_sorted_tempe)
# df_rvp_date = freyja_by_date(df_freyja_sorted_tempe)
# # resetting index because merge function sets df index to "Date" and sort_df_date function needs "Date" to be in a column
# df_freyja_date = df_freyja_date.reset_index()
# df_freyja_date = sort_df_data(df_freyja_date)

# Initializing dfs for collection site specific SARS-CoV-2 variant abundance by colletion date data.
df_asu01_RVP = location_site_date(df_site_date_RVP, 'ASUT01')
df_asu02_RVP = location_site_date(df_site_date_RVP, 'ASUT02')
df_asu03_RVP = location_site_date(df_site_date_RVP, 'ASUT03')
df_asu04_RVP = location_site_date(df_site_date_RVP, 'ASUT04')
df_asu05_RVP = location_site_date(df_site_date_RVP, 'ASUT05')
df_asu06_RVP = location_site_date(df_site_date_RVP, 'ASUT06')
df_asu07_RVP = location_site_date(df_site_date_RVP, 'ASUT07')
df_asu08_RVP = location_site_date(df_site_date_RVP, 'ASUT08')
df_asu09_RVP = location_site_date(df_site_date_RVP, 'ASUT09')
df_asu10_RVP = location_site_date(df_site_date_RVP, 'ASUT10')
df_asu11_RVP = location_site_date(df_site_date_RVP, 'ASUT11')
df_asu12_RVP = location_site_date(df_site_date_RVP, 'ASUT12')
df_asu14_RVP = location_site_date(df_site_date_RVP, 'ASUT14')
df_asu15_RVP = location_site_date(df_site_date_RVP, 'ASUT15')
df_asu16_RVP = location_site_date(df_site_date_RVP, 'ASUT16')
df_asu17_RVP = location_site_date(df_site_date_RVP, 'ASUT17')
df_asu20_RVP = location_site_date(df_site_date_RVP, 'ASUT20')
df_asu21_RVP = location_site_date(df_site_date_RVP, 'ASUT21')

# Initializing plotly express graph objects using the dfs above.
p1_RVP = site_date_bar_graph(df_asu01_RVP.tail(5), 'ASU Tempe T1 (Palo Verde)')
p2_RVP = site_date_bar_graph(df_asu02_RVP.tail(5), 'ASU Tempe T2 (Tooker C)')
p3_RVP = site_date_bar_graph(df_asu03_RVP.tail(5), 'ASU Tempe T3 (Greek)')
p4_RVP = site_date_bar_graph(df_asu04_RVP.tail(5), 'ASU Tempe T4 (Manzanita)')
p5_RVP = site_date_bar_graph(df_asu05_RVP.tail(5), 'ASU Tempe T5 (Tooker A)')
p6_RVP= site_date_bar_graph(df_asu06_RVP.tail(5), 'ASU Tempe T6 (Tooker B)')
p7_RVP = site_date_bar_graph(df_asu07_RVP.tail(5), 'ASU Tempe T7 (Hassayampa A)')
p8_RVP = site_date_bar_graph(df_asu08_RVP.tail(5), 'ASU Tempe T8 (Hassayampa B)')
p9_RVP = site_date_bar_graph(df_asu09_RVP.tail(5), 'ASU Tempe T9 (Hassayampa C)')
p10_RVP = site_date_bar_graph(df_asu10_RVP.tail(5), 'ASU Tempe T10 (Barrett College)')
p11_RVP = site_date_bar_graph(df_asu11_RVP.tail(5), 'ASU Tempe T11 (Adelphi East)')
p12_RVP = site_date_bar_graph(df_asu12_RVP.tail(5), 'ASU Tempe T12 (Adelphi Commons)')
p14_RVP = site_date_bar_graph(df_asu14_RVP.tail(5), 'ASU Tempe T14 (Best)')
p15_RVP = site_date_bar_graph(df_asu15_RVP.tail(5), 'ASU Tempe T15 (Villas at Vista)')
p16_RVP = site_date_bar_graph(df_asu16_RVP.tail(5), 'ASU Tempe T16 (Gym)')
p17_RVP = site_date_bar_graph(df_asu17_RVP.tail(5), 'ASU Tempe T17 (Hayden Library)')
p20_RVP = site_date_bar_graph(df_asu20_RVP.tail(5), 'ASU Tempe T20 (MU)')
p21_RVP = site_date_bar_graph(df_asu21_RVP.tail(5), 'ASU Tempe T21 (Student Pavilion)')


#_____RVP_read_distribution_____
infile = pd.read_csv(f'data/wastewater_virus_surveillance/combined/RVP_counts_virusOnly_normalized_filled_345.csv')
df_tempe = RVP_split_data_by_campus(infile, 'AWW', 'AWMT')
df_cumulative_all_Read_Distribution = read_distribution_data_prep(infile)
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


if check_password():
    #___formatting___
    st.sidebar.header('ASU Tempe Wastewater Virus Tracker')
    st.markdown('# ASU Tempe Campus Wastewater Virus Tracker')
    st.markdown(f"#### Today's Date: {date}")
    st.markdown(f'#### Last Updated: Mar-20-2023')
    st.markdown('---')
    st.write('''
        ### Tempe Collection Locations
        The map and table below displays Tempe campus sample collection locations and their corresponding IDs, and facilities.
        '''
        )

    col_a1, col_a2 = st.columns([3,1])
    with col_a1:
        st_data = st_folium(m, height=600, width=1000)
    with col_a2:
        st.dataframe(df_location, height=600, width=400)

    st.markdown('---')

    col_b1, col_b2 = st.columns([1,1])
    #__Freyja_graphs__
    with col_b1:
        st.markdown('### Freyja analysis')
        tab1, tab2, tab3, tab4, tab5, \
        tab6, tab7, tab8, tab9, tab10, \
        tab11, tab12, tab14, tab15, tab16,\
        tab17, tab20, tab21 = st.tabs(['T1', 'T2', 'T3', 'T4', 'T5',
                         'T6', 'T7', 'T8', 'T9', 'T10',
                         'T11', 'T12', 'T14', 'T15', 'T16',
                         'T17', 'T20', 'T21'])
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
        with tab20:
            st.plotly_chart(p20_freyja)
        with tab21:
            st.plotly_chart(p21_freyja)
    with col_b2:
        #___RVP_graphs___
        st.markdown('### RVP analysis')
        tab1, tab2, tab3, tab4, tab5, \
        tab6, tab7, tab8, tab9, tab10, \
        tab11, tab12, tab14, tab15, tab16,\
        tab17, tab20, tab21 = st.tabs(['T1', 'T2', 'T3', 'T4', 'T5',
                         'T6', 'T7', 'T8', 'T9', 'T10',
                         'T11', 'T12', 'T14', 'T15', 'T16',
                         'T17', 'T20', 'T21'])
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
        with tab20:
            st.plotly_chart(p20_RVP)
        with tab21:
            st.plotly_chart(p21_RVP)

    st.markdown('---')

    st.markdown('### Title')
    tab1, tab2 = st.tabs(['Freyja', 'RVP'])
    with tab1:
        st.plotly_chart(p_freyja_date, height=500, width=600, use_container_width=True)
        st.markdown('The graph above displays the relative abundance of currently circulating SARS-CoV-2 variants by sampling date.')
    with tab2:
        st.plotly_chart(p_ww_stacked_bar_current, height=500, width=600, use_container_width=True)
        st.markdown('The graph above displays the relative abundance of currently circulating viruses by collection date.')
    # # st.plotly_chart(p_ww_stacked_bar_historical, height=500, width=600, use_container_width=True)
    # # st.markdown('The graph above displays the relative abundance of historically circulating viruses by collection date.')
    st.markdown('---')
    st.markdown('### Viral Read Distributions at a Glance')

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

    st.dataframe(df_tempe_reads, height=248, use_container_width=True)

    st.markdown('---')
