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


date = datetime.today().strftime('%b-%d-%Y')
date2 = datetime.today().strftime('%y%m%d')

st.set_page_config(
    page_title='Tempe Campus',
    page_icon='🚱',
    layout='wide'
)

def check_password():
    '''Returns `True` if the user had a correct password.'''
    def password_entered():
        '''Checks whether a password entered by the user is correct.'''
        if (
            st.session_state["username"] in st.secrets["passwords"]
            and st.session_state["password"]
            == st.secrets["passwords"][st.session_state["username"]]
        ):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store username + password
            del st.session_state["username"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show inputs for username + password.
        st.text_input("Username", on_change=password_entered, key="username")
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.text_input("Username", on_change=password_entered, key="username")
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        st.error("User not known or password incorrect")
        return False
    else:
        # Password correct.
        return True


@st.cache_data
def ww_stacked_bar():
    df = pd.read_csv('data/dataframes/TempeWW_test.csv')
    df['Week'] = pd.to_datetime(df['Week']).dt.strftime('%b %d %y')
    df = df.set_index('Week')
    df = df.loc[:, 'SARS-CoV-2':'West Nile virus']
    df = df.applymap(lambda x: x if not np.isnan(x)
                       else np.random.choice(range(10)))
    return df


@st.cache_data
def tempe_locations():
    df = pd.read_csv('data/wastewater_virus_surveillance/tempe/tempe_locations.csv')
    df = df.set_index('ID')
    return df


@st.cache_data
def tempe_read_distribution():
    df = pd.read_csv('data/wastewater_virus_surveillance/tempe/tempe_read_distribution_table.csv')
    df = df.set_index('Date')
    return df


@st.cache_data
def freyja_by_date():
    df = pd.read_csv('data/wastewater_virus_surveillance/tempe/freyja/freyja_grouped_avg_by_date_tempe.csv')
    return df


@st.cache_data
def freyja_by_site():
    df = pd.read_csv('data/wastewater_virus_surveillance/tempe/freyja/freyja_grouped_avg_by_site_tempe.csv')
    df = df.set_index('Site')
    return df


@st.cache_data
def freyja_location_abundance_by_date():
    df = pd.read_csv('data/wastewater_virus_surveillance/combined/Combined_freyja_grouped_metadata_analysis.csv')
    df = df.iloc[:, 2:]
    df = df.set_index(['Site', 'Date'])
    df = df[col_list]
    df = df.reset_index()
    return df


def sort_df_data(df):
    df['Date'] = df['Date'].astype(str)
    new_dates = []
    for i in df['Date']:
        j = i[:2] + '-' + i[2:4] + '-' + i[4:]
        k = j.split('-')
        l = k[1] + '-' + k[2] + '-' + k[0]
        new_dates.append(l)
    df['Date'] = new_dates
    df['Date'] = df['Date'].sort_values()
    df['Date'] = pd.to_datetime(df['Date'])
    df['Date'] = df['Date'].dt.strftime('%b-%d-%y')
    df = df.set_index('Date')
    return df


@st.cache_data
def sort_csv_data():
    df = pd.read_csv('data/dataframes/weekly_counts_avg_230314.csv')
    df['Date'] = df['Date'].astype(str)
    new_dates = []
    for i in df['Date']:
        j = i[:2] + '-' + i[2:4] + '-' + i[4:]
        k = j.split('-')
        l = k[1] + '-' + k[2] + '-' + k[0]
        new_dates.append(l)
        # print(i, j, k, l)
    df['Date'] = new_dates
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.set_index('Date')
    return df


@st.cache_data
def organize_df(df):
    date_list = [i for i in df.columns]
    df1 = pd.DataFrame({
    'Week': date_list,
    'Adenovirus': df.iloc[0].tolist(),
    'Bocavirus': df.iloc[1].tolist(),
    'Coronavirus': df.iloc[2].tolist(),
    'Enterovirus': df.iloc[3].tolist(),
    'Metapneumovirus': df.iloc[4].tolist(),
    'Parainfluenza': df.iloc[5].tolist(),
    'Parechovirus':  df.iloc[6].tolist(),
    'RSV': df.iloc[7].tolist(),
    'Rhinovirus': df.iloc[8].tolist(),
    'Rubulavirus': df.iloc[9].tolist(),
    'Influenza': df.iloc[10].tolist(),
    'Polyomavirus': df.iloc[11].tolist(),
    'SARS-CoV-2': df.iloc[12].tolist(),
    })
    df_melt = df1.melt(id_vars=['Week'], var_name='Circulating pathogens',
                       value_name='Amount', value_vars=df1.columns[1:], ignore_index=True)
    df_melt['%'] = 100 * df_melt['Amount'] /\
        df_melt.groupby('Week')['Amount'].transform('sum')
    return df_melt


#___retrieve_image____
adeno_historical = Image.open('data/wastewater_virus_surveillance/images/historical/grouped_counts_Adenovirus_scatter.png')
adeno_current = Image.open('data/wastewater_virus_surveillance/images/current/tempe/scatter/weekly_counts_Adenovirus_scatter.png')
cov2_historical = Image.open('data/wastewater_virus_surveillance/images/historical/grouped_counts_SARS-CoV-2_scatter.png')
cov2_current = Image.open('data/wastewater_virus_surveillance/images/current/tempe/scatter/weekly_counts_SARS-CoV-2_scatter.png')
flu_historial = Image.open('data/wastewater_virus_surveillance/images/historical/grouped_counts_Influenza_scatter.png')
flu_current = Image.open('data/wastewater_virus_surveillance/images/current/tempe/scatter/weekly_counts_Influenza_scatter.png')

col_list = ['XBB', 'XBB.1.5', 'BQ.1', 'BQ.1.1', 'B.1.1.529',
            'BA.1.1', 'BA.2', 'BA.2.12.1', 'BA.2.75', 'BA.2.75.2',
            'BN.1', 'BA.4', 'BA.4.6', 'BA.5', 'BA.5.2.6', 'BF.7',
            'BF.11', 'Delta', 'Other_recombinants', 'Other', 'Filtered_reads']

colors1 = ['#7f7f7f', '#d62728', '#aec7e8', '#8c564b', '#2ca02c',
          '#ff7f0e', '#c49c94', '#ff9896', '#9467bd', '#c5b0d5',
          '#ffbb78', '#98df8a', '#1f77b4']

colors2 = ['#0066FF', '#7CB1FF', '#ff7f0e', '#ffbb78', '#2ca02c',
          '#98df8a', '#d62728', '#ff9896', '#A633B8', '#9467bd',
          '#c5b0d5', '#8c564b', '#c49c94', '#e377c2', '#f7b6d2',
          '#7f7f7f', '#c7c7c7', '#bcbd22', '#aec7e8', '#F2B880',
          '#FFE677']



#____processing_____
df_tempe_data = sort_csv_data().tail(6).copy()
df_tempe_data = df_tempe_data.reset_index()
date_list = [i.strftime('%b-%d-%Y') for i in df_tempe_data['Date']]
df_tempe_data['Date'] = date_list
df_tempe_data = df_tempe_data.set_index('Date')
df_tempe_data1 = df_tempe_data.T.copy()
df_tempe_data1 = organize_df(df_tempe_data1)
date_list = [i for i in df_tempe_data1['Week']]

#____map____
latitudes_list = [33.418298, 33.422039, 33.423573, 33.418049, 33.422113,
                  33.423294, 33.422863, 33.416281, 33.415880, 33.415257,
                  33.414915, 33.412871, 33.412884, 33.416039, 33.414170,
                  33.415984, 33.419664]

longitudes_list = [-111.932704, -111.933943, -111.933783, -111.926203, -111.930186,
                   -111.933761, -111.933746, -111.929055, -111.930002, -111.930380,
                   -111.928599, -111.927151, -111.927948, -111.935788, -111.931554,
                   -111.932021, -111.935681]

popups = ['ASU Tempe', 'T1', 'T2', 'T3', 'T4',
          'T5', 'T6', 'T7', 'T8', 'T9', 'T10',
          'T11', 'T12', 'T14', 'T15', 'T16',
          'T17']

tooltips = ['ASU Tempe', 'T1', 'T2', 'T3', 'T4',
            'T5', 'T6', 'T7', 'T8', 'T9', 'T10',
            'T11', 'T12', 'T14', 'T15', 'T16',
            'T17']

# Center at latitude/longitude coordinates.
m = folium.Map(location=[33.418298, -111.932704], zoom_start=15)

# Add markers
for i, j, k, l in zip(latitudes_list, longitudes_list, popups, tooltips):
    folium.Marker(
                location=[i, j],
                popup=k,
                tooltip=l,
                icon=folium.Icon(color='orange')

    ).add_to(m)


#____initializing_dfs_____
df_ww_stacked_bar = ww_stacked_bar()
df_tempe_locations = tempe_locations()
df_tempe_reads = tempe_read_distribution()
df_freyja_date = freyja_by_date()
df_freyja_date = sort_df_data(df_freyja_date)
df_freyja_site = freyja_by_site()
df_freyja_tempe_site = df_freyja_site[:-6]
df_tempe_locations = tempe_locations()


#_____freyja_____
df_freyja_date = df_freyja_date[col_list]
df_freyja_date = df_freyja_date.T
week_list = [i for i in df_freyja_date.columns]

df_freyja_date2 = pd.DataFrame({
    'Date': week_list,
    'XBB': df_freyja_date.iloc[0].tolist(),
    'XBB.1.5': df_freyja_date.iloc[1].tolist(),
    'BQ.1': df_freyja_date.iloc[2].tolist(),
    'BQ.1.1': df_freyja_date.iloc[3].tolist(),
    'B.1.1.529': df_freyja_date.iloc[4].tolist(),
    'BA.1.1': df_freyja_date.iloc[5].tolist(),
    'BA.2':  df_freyja_date.iloc[6].tolist(),
    'BA.2.12.1': df_freyja_date.iloc[7].tolist(),
    'BA.2.75': df_freyja_date.iloc[8].tolist(),
    'BA.2.75.2': df_freyja_date.iloc[9].tolist(),
    'BN.1': df_freyja_date.iloc[10].tolist(),
    'BA.4': df_freyja_date.iloc[11].tolist(),
    'BA.4.6': df_freyja_date.iloc[12].tolist(),
    'BA.5': df_freyja_date.iloc[13].tolist(),
    'BA.5.2.6': df_freyja_date.iloc[14].tolist(),
    'BF.7': df_freyja_date.iloc[15].tolist(),
    'BF.11': df_freyja_date.iloc[16].tolist(),
    'Delta': df_freyja_date.iloc[17].tolist(),
    'Other recombinants': df_freyja_date.iloc[18].tolist(),
    'Other variants': df_freyja_date.iloc[19].tolist(),
    'Filtered_reads': df_freyja_date.iloc[20].tolist(),
    })

df_melt1 = df_freyja_date2.melt(id_vars=['Date'], var_name='Variant',
                   value_name='Amount', value_vars=df_freyja_date2.columns[1:], ignore_index=True)
df_melt1['%'] = 100 * df_melt1['Amount'] /\
    df_melt1.groupby('Date')['Amount'].transform('sum')


df_freyja_site = df_freyja_site[col_list]
df_freyja_site = df_freyja_site.T
site = [i for i in df_freyja_site.columns]


df_freyja_site2 = pd.DataFrame({
    'Site': site,
    'XBB': df_freyja_site.iloc[0].tolist(),
    'XBB.1.5': df_freyja_site.iloc[1].tolist(),
    'BQ.1': df_freyja_site.iloc[2].tolist(),
    'BQ.1.1': df_freyja_site.iloc[3].tolist(),
    'B.1.1.529': df_freyja_site.iloc[4].tolist(),
    'BA.1.1': df_freyja_site.iloc[5].tolist(),
    'BA.2':  df_freyja_site.iloc[6].tolist(),
    'BA.2.12.1': df_freyja_site.iloc[7].tolist(),
    'BA.2.75': df_freyja_site.iloc[8].tolist(),
    'BA.2.75.2': df_freyja_site.iloc[9].tolist(),
    'BN.1': df_freyja_site.iloc[10].tolist(),
    'BA.4': df_freyja_site.iloc[11].tolist(),
    'BA.4.6': df_freyja_site.iloc[12].tolist(),
    'BA.5': df_freyja_site.iloc[13].tolist(),
    'BA.5.2.6': df_freyja_site.iloc[14].tolist(),
    'BF.7': df_freyja_site.iloc[15].tolist(),
    'BF.11': df_freyja_site.iloc[16].tolist(),
    'Delta': df_freyja_site.iloc[17].tolist(),
    'Other recombinants': df_freyja_site.iloc[18].tolist(),
    'Other variants': df_freyja_site.iloc[19].tolist(),
    'Filtered_reads': df_freyja_site.iloc[20].tolist(),
    })


df_melt2 = df_freyja_site2.melt(id_vars=['Site'], var_name='Variant',
                   value_name='Amount', value_vars=df_freyja_site2.columns[1:], ignore_index=True)
df_melt2['%'] = 100 * df_melt2['Amount'] /\
    df_melt2.groupby('Site')['Amount'].transform('sum')

#____Tempe_location_abundance_by_date_____
df_site_date = freyja_location_abundance_by_date()

df_asu01 = sort_df_data(df_site_date[df_site_date['Site'].str.startswith('ASUT01')].drop(columns=['Site']))
df_asu02 = sort_df_data(df_site_date[df_site_date['Site'].str.startswith('ASUT02')].drop(columns=['Site']))
df_asu03 = sort_df_data(df_site_date[df_site_date['Site'].str.startswith('ASUT03')].drop(columns=['Site']))
df_asu04 = sort_df_data(df_site_date[df_site_date['Site'].str.startswith('ASUT04')].drop(columns=['Site']))
df_asu05 = sort_df_data(df_site_date[df_site_date['Site'].str.startswith('ASUT05')].drop(columns=['Site']))
df_asu06 = sort_df_data(df_site_date[df_site_date['Site'].str.startswith('ASUT06')].drop(columns=['Site']))
df_asu07 = sort_df_data(df_site_date[df_site_date['Site'].str.startswith('ASUT07')].drop(columns=['Site']))
df_asu08 = sort_df_data(df_site_date[df_site_date['Site'].str.startswith('ASUT08')].drop(columns=['Site']))
df_asu09 = sort_df_data(df_site_date[df_site_date['Site'].str.startswith('ASUT09')].drop(columns=['Site']))
df_asu10 = sort_df_data(df_site_date[df_site_date['Site'].str.startswith('ASUT10')].drop(columns=['Site']))
df_asu11 = sort_df_data(df_site_date[df_site_date['Site'].str.startswith('ASUT11')].drop(columns=['Site']))
df_asu12 = sort_df_data(df_site_date[df_site_date['Site'].str.startswith('ASUT12')].drop(columns=['Site']))
df_asu14 = sort_df_data(df_site_date[df_site_date['Site'].str.startswith('ASUT14')].drop(columns=['Site']))
df_asu15 = sort_df_data(df_site_date[df_site_date['Site'].str.startswith('ASUT15')].drop(columns=['Site']))
df_asu16 = sort_df_data(df_site_date[df_site_date['Site'].str.startswith('ASUT16')].drop(columns=['Site']))
df_asu17 = sort_df_data(df_site_date[df_site_date['Site'].str.startswith('ASUT17')].drop(columns=['Site']))


#____plotly_graphing____
p_freyja_date = px.bar(df_melt1,
                        x='Date',
                        y='%',
                        color_discrete_sequence=colors2,
                        color='Variant',
                        title='ASU Tempe Wastewater SARS-CoV-2 Variants by Date',
                        # template='plotly_dark'
                        )

p_freyja_date.update_layout(barmode='relative',
                             xaxis=dict(
                                 ticks='outside',
                                 tickson='boundaries',
                                 tickangle=-45,
                                 tickmode='auto',
                                 # tick0=0.1,
                                 # dtick=0.2
                             ),
                             # autosize=True,
                             width=900,
                             height=610,
                             # paper_bgcolor='rgba(0,0,0,0)',
                             plot_bgcolor='rgba(0,0,0,0)'
                             )

p_freyja_site = px.bar(df_melt2,
                       x='Site',
                       y='%',
                       color_discrete_sequence=colors2,
                       color='Variant',
                       title='ASU Tempe Wastewater SARS-CoV-2 Variants by Location',
                       # template='plotly_dark'
                       )

p_freyja_site.update_layout(barmode='relative',
                        xaxis=dict(
                            tickangle=-45,
                            tickson='boundaries',
                            tickmode='linear'
                            # tick0=0.1,
                            # dtick=0.2
                        ),
                        xaxis_title='Location',
                        # autosize=True,
                        width=900,
                        height=610,
                        # paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)'
                    )

p_ww_stacked_bar_historical = go.Figure(
    data=px.bar(df_ww_stacked_bar,
                color='variable',
                # text='variable', # get feedback
                title='Historically Ciruculating Viruses in ASU Tempe Wastewater',
                labels={
                    'value': 'Relative virus abundance',
                    'Week': 'Week',
                    'variable': '10 High-risk pathogens'},
                # template='plotly_dark'
                )
            )

p_ww_stacked_bar_historical.update_layout(
    # hovermode='x', # get feedback
    # hovermode='x unified', # get feedback
    xaxis=dict(
        tickangle=-45,
    ),
    autosize=True,
    plot_bgcolor='rgba(0,0,0,0)'
)
p_ww_stacked_bar_current = px.bar(df_tempe_data1,
                                  x='Week',
                                  y='%',
                                  color_discrete_sequence= colors1,
                                  color='Circulating pathogens',
                                  title='Circulating Viruses in ASU Tempe Wastewater',
                                  # template='plotly_dark'
)

p_ww_stacked_bar_current.update_layout(barmode='relative',
                                       xaxis=dict(
                                           tickangle=-45,
                                           # tick0=0.1,
                                           # dtick=0.2
                                       ),
                                       xaxis_title='Date',
                                       autosize=True,
                                       # width=900,
                                       # height=500,
)


#____Tempe_location_abundance_by_date_graphing_____
##___outputadjustment____
tickangle = -45
p_width = 500
p_hight = 500
yaxis_title = '% abundance'
xaxis_title = 'Collection Date'

p1 = px.bar(df_asu01,
            color_discrete_sequence=colors2,
            title='ASU Tempe T1 (Palo Verde)'
            )
p2 = px.bar(df_asu02,
            color_discrete_sequence=colors2,
            title='ASU Tempe T2 (Tooker C)',
            )
p3 = px.bar(df_asu03,
            color_discrete_sequence=colors2,
            title='ASU Tempe T3 (Greek)',
            )
p4 = px.bar(df_asu04,
            color_discrete_sequence=colors2,
            title='ASU Tempe T4 (Manzanita)',
            )
p5 = px.bar(df_asu05,
            color_discrete_sequence=colors2,
            title='ASU Tempe T5 (Tooker A)',
            )
p6 = px.bar(df_asu06,
            color_discrete_sequence=colors2,
            title='ASU Tempe T6 (Palo Verde)',
            )
p7 = px.bar(df_asu07,
            color_discrete_sequence=colors2,
            title='ASU Tempe T7 (Palo Verde)',
            )
p8 = px.bar(df_asu08,
            color_discrete_sequence=colors2,
            title='ASU Tempe T8 (Palo Verde)',
            )
p9 = px.bar(df_asu09,
            color_discrete_sequence=colors2,
            title='ASU Tempe T9 (Palo Verde)',
            )
p10 = px.bar(df_asu10,
            color_discrete_sequence=colors2,
            title='ASU Tempe T10 (Palo Verde)',
            )
p11 = px.bar(df_asu11,
            color_discrete_sequence=colors2,
            title='ASU Tempe T11 (Palo Verde)',
            )
p12 = px.bar(df_asu12,
            color_discrete_sequence=colors2,
            title='ASU Tempe T12 (Palo Verde)',
            )
p14 = px.bar(df_asu14,
            color_discrete_sequence=colors2,
            title='ASU Tempe T14 (Palo Verde)',
            )
p15 = px.bar(df_asu15,
            color_discrete_sequence=colors2,
            title='ASU Tempe T15 (Palo Verde)',
            )
p16 = px.bar(df_asu16,
            color_discrete_sequence=colors2,
            title='ASU Tempe T16 (Palo Verde)',
            )
p17 = px.bar(df_asu17,
            color_discrete_sequence=colors2,
            title='ASU Tempe T17 (Palo Verde)',
            )


p1.update_layout(barmode='relative',
                        xaxis=dict(
                            tickangle=tickangle,
                            tickson='boundaries',
                            tickmode='linear'
                        ),
                        yaxis_title=yaxis_title,
                        xaxis_title=xaxis_title,
                        width=p_width,
                        height=p_hight,
                    )
p2.update_layout(barmode='relative',
                        xaxis=dict(
                            tickangle=tickangle,
                            tickson='boundaries',
                            tickmode='linear'
                        ),
                        yaxis_title=yaxis_title,
                        xaxis_title=xaxis_title,
                        width=p_width,
                        height=p_hight,
                    )
p3.update_layout(barmode='relative',
                        xaxis=dict(
                            tickangle=tickangle,
                            tickson='boundaries',
                            tickmode='linear'
                        ),
                        yaxis_title=yaxis_title,
                        xaxis_title=xaxis_title,
                        width=p_width,
                        height=p_hight,
                    )
p4.update_layout(barmode='relative',
                        xaxis=dict(
                            tickangle=tickangle,
                            tickson='boundaries',
                            tickmode='linear'
                        ),
                        yaxis_title=yaxis_title,
                        xaxis_title=xaxis_title,
                        width=p_width,
                        height=p_hight,
                    )
p5.update_layout(barmode='relative',
                        xaxis=dict(
                            tickangle=tickangle,
                            tickson='boundaries',
                            tickmode='linear'
                        ),
                        yaxis_title=yaxis_title,
                        xaxis_title=xaxis_title,
                        width=p_width,
                        height=p_hight,
                    )
p6.update_layout(barmode='relative',
                        xaxis=dict(
                            tickangle=tickangle,
                            tickson='boundaries',
                            tickmode='linear'
                        ),
                        yaxis_title=yaxis_title,
                        xaxis_title=xaxis_title,
                        width=p_width,
                        height=p_hight,
                    )
p7.update_layout(barmode='relative',
                        xaxis=dict(
                            tickangle=tickangle,
                            tickson='boundaries',
                            tickmode='linear'
                        ),
                        yaxis_title=yaxis_title,
                        xaxis_title=xaxis_title,
                        width=p_width,
                        height=p_hight,
                    )
p8.update_layout(barmode='relative',
                        xaxis=dict(
                            tickangle=tickangle,
                            tickson='boundaries',
                            tickmode='linear'
                        ),
                        yaxis_title=yaxis_title,
                        xaxis_title=xaxis_title,
                        width=p_width,
                        height=p_hight,
                    )
p9.update_layout(barmode='relative',
                        xaxis=dict(
                            tickangle=tickangle,
                            tickson='boundaries',
                            tickmode='linear'
                        ),
                        yaxis_title=yaxis_title,
                        xaxis_title=xaxis_title,
                        width=p_width,
                        height=p_hight,
                    )
p10.update_layout(barmode='relative',
                        xaxis=dict(
                            tickangle=tickangle,
                            tickson='boundaries',
                            tickmode='linear'
                        ),
                        yaxis_title=yaxis_title,
                        xaxis_title=xaxis_title,
                        width=p_width,
                        height=p_hight,
                    )
p11.update_layout(barmode='relative',
                        xaxis=dict(
                            tickangle=tickangle,
                            tickson='boundaries',
                            tickmode='linear'
                        ),
                        yaxis_title=yaxis_title,
                        xaxis_title=xaxis_title,
                        width=p_width,
                        height=p_hight,
                    )
p12.update_layout(barmode='relative',
                        xaxis=dict(
                            tickangle=tickangle,
                            tickson='boundaries',
                            tickmode='linear'
                        ),
                        yaxis_title=yaxis_title,
                        xaxis_title=xaxis_title,
                        width=p_width,
                        height=p_hight,
                    )
p14.update_layout(barmode='relative',
                        xaxis=dict(
                            tickangle=tickangle,
                            tickson='boundaries',
                            tickmode='linear'
                        ),
                        yaxis_title=yaxis_title,
                        xaxis_title=xaxis_title,
                        width=p_width,
                        height=p_hight,
                    )
p15.update_layout(barmode='relative',
                        xaxis=dict(
                            tickangle=tickangle,
                            tickson='boundaries',
                            tickmode='linear'
                        ),
                        yaxis_title=yaxis_title,
                        xaxis_title=xaxis_title,
                        width=p_width,
                        height=p_hight,
                    )
p16.update_layout(barmode='relative',
                        xaxis=dict(
                            tickangle=tickangle,
                            tickson='boundaries',
                            tickmode='linear'
                        ),
                        yaxis_title=yaxis_title,
                        xaxis_title=xaxis_title,
                        width=p_width,
                        height=p_hight,
                    )
p17.update_layout(barmode='relative',
                        xaxis=dict(
                            tickangle=tickangle,
                            tickson='boundaries',
                            tickmode='linear'
                        ),
                        yaxis_title=yaxis_title,
                        xaxis_title=xaxis_title,
                        width=p_width,
                        height=p_hight,
                    )


#___adding_bar_graph_outline___
for i in range(len(df_ww_stacked_bar.columns)):
    p_ww_stacked_bar_historical.data[i].marker.line.width = 0.8
    p_ww_stacked_bar_historical.data[i].marker.line.color = 'black'

for i in range(len(df_melt1.columns)):
    p_freyja_date.data[i].marker.line.width = 0.8
    p_freyja_date.data[i].marker.line.color = 'black'

for i in range(len(df_melt2.columns)):
    p_freyja_site.data[i].marker.line.width = 0.8
    p_freyja_site.data[i].marker.line.color = 'black'

for i in range(len(df_tempe_data1.columns)):
    p_ww_stacked_bar_current.data[i].marker.line.width = 0.8
    p_ww_stacked_bar_current.data[i].marker.line.color = 'black'

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

    col_a1, col_a2, col_a3 = st.columns(3)
    with col_a1:
        st_data = st_folium(m, height=500, width=500)

    with col_a2:
        st.dataframe(df_tempe_locations, height=500, width=400)

    with col_a3:
        tab1, tab2, tab3, tab4, tab5, \
        tab6, tab7, tab8, tab9, tab10, \
        tab11, tab12, tab14, tab15, tab16,\
        tab17 = st.tabs(['T1', 'T2', 'T3', 'T4', 'T5',
                         'T6', 'T7', 'T8', 'T9', 'T10',
                         'T11', 'T12', 'T14', 'T15', 'T16',
                         'T17'])
        with tab1:
            st.plotly_chart(p1)
        with tab2:
            st.plotly_chart(p2)
        with tab3:
            st.plotly_chart(p3)
        with tab4:
            st.plotly_chart(p4)
        with tab5:
            st.plotly_chart(p5)
        with tab6:
            st.plotly_chart(p6)
        with tab7:
            st.plotly_chart(p7)
        with tab8:
            st.plotly_chart(p8)
        with tab9:
            st.plotly_chart(p9)
        with tab10:
            st.plotly_chart(p10)
        with tab11:
            st.plotly_chart(p11)
        with tab12:
            st.plotly_chart(p12)
        with tab14:
            st.plotly_chart(p14)
        with tab15:
            st.plotly_chart(p15)
        with tab16:
            st.plotly_chart(p16)
        with tab17:
            st.plotly_chart(p17)

    st.markdown('---')
    st.markdown('### Tempe Wastewater SARS-CoV-2 Freyja Analysis')

    #___freyja_data___
    st.plotly_chart(p_freyja_site, height=500, width=600, use_container_width=True)
    st.markdown('The graph above displays the relative abundance of currently circulating SARS-CoV-2 variants by sampling location.')
    st.plotly_chart(p_freyja_date, height=500, width=600, use_container_width=True)
    st.markdown('The graph above displays the relative abundance of currently circulating SARS-CoV-2 variants by sampling date.')
    st.markdown('---')
    st.markdown('### Tempe wastewater RVP Analysis')
    st.plotly_chart(p_ww_stacked_bar_current, height=500, width=600, use_container_width=True)
    st.markdown('The graph above displays the relative abundance of currently circulating viruses by collection date.')
    st.plotly_chart(p_ww_stacked_bar_historical, height=500, width=600, use_container_width=True)
    st.markdown('The graph above displays the relative abundance of historically circulating viruses by collection date.')
    st.markdown('---')
    st.markdown('### Viral Read Distributions at a Glance')

    #_____read_distribution_data______
    col_b1, col_b2, col_b3  = st.columns(3)

    with col_b1:
        st.image(adeno_historical)
        st.image(adeno_current)

    with col_b2:
        st.image(cov2_historical)
        st.image(cov2_current)

    with col_b3:
        st.image(flu_historial)
        st.image(flu_current)

    st.dataframe(df_tempe_reads, height=248, use_container_width=True)

    st.markdown('---')
