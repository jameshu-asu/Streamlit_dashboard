import pandas as pd
import numpy as np
import folium
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import datetime
from datetime import datetime
from streamlit_folium import st_folium
from PIL import Image
from typing import Final


'''By James C. Hu
Collection of funcitons used to generate dashboard visualizations.
'''

run = 350
GISAID_update_date = 'Aug-29-2023'
ww_update_date = 'Jun-21-2023'
spike_mutation_tracker = 'May-23-2023'


date1 = datetime.today().strftime('%b-%d-%Y')

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


def test():
    return print('import successful')

# possible locaitons tempe, polytechnic, west, downtown


@st.cache_data
def locations(location: str):
    df = pd.read_csv(f'data/wastewater_virus_surveillance/{location}/{location}_locations.csv')
    df = df.set_index('ID')
    return df


# possible locaitons tempe, polytechnic, west, downtown
@st.cache_data
def read_distribution(location: str):
    df = pd.read_csv(f'data/wastewater_virus_surveillance/{location}/{location}_read_distribution_table.csv')
    df = df.set_index('Date')
    return df


# location_code Tempe: ASUT, Polytechnic: ASUP, West: ASUW, Downtown: ASUDT
@st.cache_data
def freyja_sort_by_location(df, *location_code: str):
    df = df[df['Site'].str.startswith((location_code))]
    df = df.set_index(['Site', 'Date', 'COVIDSeq_Seq_ID', 'Sample_ID'])
    df = df[col_list]
    df = df.reset_index()
    return df


@st.cache_data
def freyja_by_site(df):
    df1 = df.drop(columns=['COVIDSeq_Seq_ID', 'Sample_ID', 'Date'])
    df1 = df1.groupby(['Site'])
    df1 = df1.mean()
    return df1


@st.cache_data
def freyja_by_date(df):
    df1 = df.drop(columns=['COVIDSeq_Seq_ID', 'Sample_ID', 'Site'])
    df1 = df1.groupby(['Date'])
    df1 = df1.mean()
    return df1


@st.cache_data
def freyja_by_site_date(df):
    df1 = df.drop(columns=['COVIDSeq_Seq_ID', 'Sample_ID'])
    df1 = df1.set_index(['Site', 'Date'])
    df1 = df1[col_list]
    df1 = df1.reset_index()
    return df1


@st.cache_data
def RVP_sort_by_location(df, location_code: str):
    df = df[df['Site'].str.startswith(location_code)]
    df = df.set_index(['Site', 'Date', 'Respiratory_Seq_ID', 'External_ID'])
    df = df.reset_index()
    return df


@st.cache_data
def RVP_by_site(df):
    df1 = df.drop(columns=['Respiratory_Seq_ID', 'External_ID', 'Date'])
    df1 = df1.groupby(['Site'])
    df1 = df1.mean()
    return df1


@st.cache_data
def RVP_by_date(df):
    df1 = df.drop(columns=['Respiratory_Seq_ID', 'External_ID', 'Site'])
    df1 = df1.groupby(['Date'])
    df1 = df1.mean()
    return df1


@st.cache_data
def RVP_by_site_date(df):
    df1 = df.drop(columns=['Respiratory_Seq_ID', 'External_ID'])
    df1 = df1.set_index(['Site', 'Date'])
    df1 = df1.reset_index()
    return df1


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
    df['Date'] = df['Date'].dt.strftime('%b-%d-%Y')
    df = df.set_index('Date')
    return df


@st.cache_data
def sort_csv_data(infile):
    df = pd.read_csv(infile)
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
def organize_df_by_virus(df):
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


@st.cache_data
def melt_df(df, category, var_name: str):
    df_melt = df.melt(id_vars=[category], var_name=var_name,
                      value_name='Amount', value_vars=df.columns[1:], ignore_index=True)
    df_melt['%'] = 100 * df_melt['Amount'] /\
        df_melt.groupby(category)['Amount'].transform('sum')
    return df_melt


@st.cache_data
def freyja_location_site_by_date(df, *category: str):
    df1 = df[df['Site'].str.startswith((category))]
    df2 = freyja_by_date(df1).reset_index().tail(5)
    df3 = melt_df(df2, 'Date', 'Variants')
    df3 = sort_df_data(df3).reset_index()
    return df3


@st.cache_data
def RVP_location_site_by_date(df, *category: str):
    df1 = df[df['Site'].str.startswith((category))]
    df2 = group_by_date(df1).drop(columns='index').reset_index().tail(5)
    df3 = melt_df(df2, 'Date', 'Circulating pathogens')
    df3 = sort_df_data(df3).reset_index()
    return df3

# category can be Site or Date, case sensitive here


@st.cache_data
def organize_df(df, category):
    df = df[col_list]
    df = df.T
    column_names = [i for i in df.columns]

    df2 = pd.DataFrame({
        category: column_names,
        'XBB': df.iloc[0].tolist(),
        'XBB.1.5': df.iloc[1].tolist(),
        'BQ.1': df.iloc[2].tolist(),
        'BQ.1.1': df.iloc[3].tolist(),
        'B.1.1.529': df.iloc[4].tolist(),
        'BA.1.1': df.iloc[5].tolist(),
        'BA.2':  df.iloc[6].tolist(),
        'BA.2.12.1': df.iloc[7].tolist(),
        'BA.2.75': df.iloc[8].tolist(),
        'BA.2.75.2': df.iloc[9].tolist(),
        'BN.1': df.iloc[10].tolist(),
        'BA.4': df.iloc[11].tolist(),
        'BA.4.6': df.iloc[12].tolist(),
        'BA.5': df.iloc[13].tolist(),
        'BA.5.2.6': df.iloc[14].tolist(),
        'BF.7': df.iloc[15].tolist(),
        'BF.11': df.iloc[16].tolist(),
        'Delta': df.iloc[17].tolist(),
        'Other recombinants': df.iloc[18].tolist(),
        'Other variants': df.iloc[19].tolist(),
        # 'Filtered_reads': df.iloc[20].tolist(),
    })

    df_melt = df2.melt(id_vars=[category], var_name='Variant',
                       value_name='Amount', value_vars=df2.columns[1:], ignore_index=True)
    df_melt['%'] = 100 * df_melt['Amount'] /\
        df_melt.groupby(category)['Amount'].transform('sum')
    return df_melt


# category1 can be Site or Date, category2 is for what gets colored currently 'Variant' or 'Circulating pathogens'
@st.cache_data
def location_date_bar_graph(df, category1: str, category2: str, graph_title: str, width: int, height: int):
    p = px.bar(df,
               x=category1,
               y='%',
               color_discrete_sequence=colors2,
               color=category2,
               title=graph_title,
               # template='plotly_dark'
               )

    p.update_layout(barmode='relative',
                    xaxis=dict(
                        ticks='outside',
                        tickson='boundaries',
                        tickangle=-45,
                        tickmode='auto',
                        # tick0=0.1,
                        # dtick=0.2
                    ),
                    # autosize=True,
                    width=width,
                    height=height,
                    yaxis_title='% abundance',
                    xaxis_title='Collection Date',
                    )
    return p


@st.cache_data
def site_date_bar_graph(df, graph_title: str):
    p = px.bar(df,
               color_discrete_sequence=colors2,
               title=graph_title
               )
    p.update_layout(barmode='relative',
                            xaxis=dict(
                                tickangle=-45,
                                tickson='boundaries',
                                tickmode='linear'
                            ),
                    yaxis_title='% abundance',
                    xaxis_title='Collection Date',
                    width=500,
                    height=500,
                    )
    return p


@st.cache_data
def stacked_bar_graph(df):
    p = px.bar(df,
               x='Week',
               y='%',
               color_discrete_sequence=colors2[:13],
               color='Circulating pathogens',
               title='Circulating Viruses in ASU Tempe Wastewater',
               # template='plotly_dark'
               )

    p.update_layout(barmode='relative',
                    xaxis=dict(
                        tickangle=-45,
                        # tick0=0.1,
                        # dtick=0.2
                    ),
                    yaxis_title='% abundance',
                    xaxis_title='Collection Date',
                    autosize=True,
                    # width=900,
                    height=500,
                    )
    return p


#_____RVP_____
virus_dict = {'Human adenovirus B1': 'Human_adenovirus_B1', 'Human adenovirus C': 'Human_adenovirus_C', 'Human adenovirus E': 'Human_adenovirus_E',
              'Human bocavirus 2c PK isolate PK-5510': 'Human_bocavirus_2c_PK_isolate_PK-5510', 'Human bocavirus 3': 'Human_bocavirus_3', 'Human bocavirus 4 NI strain HBoV4-NI-385': 'Human_bocavirus_4_NI_strain_HBoV4-NI-385', 'Primate bocaparvovirus 1 isolate st2': 'Primate_bocaparvovirus_1_isolate_st2',
              'Human coronavirus 229E': 'Human_coronavirus_229E', 'Human coronavirus HKU1': 'Human_coronavirus_HKU1', 'Human Coronavirus NL63': 'Human_Coronavirus_NL63', 'Human coronavirus OC43': 'Human_coronavirus_OC43',
              'Enterovirus C104': 'Enterovirus_C104', 'Human enterovirus 109': 'Human_enterovirus_109',
              'Human metapneumovirus': 'Human_metapneumovirus',
              'Human parainfluenza virus 1': 'Human_parainfluenza_virus_1', 'Human parainfluenza virus 3': 'Human_parainfluenza_virus_3', 'Human parainfluenza virus 4a': 'Human_parainfluenza_virus_4a',
              'Human parechovirus 6': 'Human_parechovirus_6', 'Human parechovirus type 1 PicoBank/HPeV1/a': 'Human_parechovirus_type_1_PicoBank/HPeV1/a',
              'Human Respiratory syncytial virus 9320': 'Human_Respiratory_syncytial_virus_9320', 'Respiratory syncytial virus': 'Respiratory_syncytial_virus',
              'Human rhinovirus 89': 'Human_rhinovirus_89', 'Human rhinovirus C': 'Human_rhinovirus_C', 'Rhinovirus B14': 'Rhinovirus_B14',
              'Human rubulavirus 2': 'Human_rubulavirus_2',
              'Influenza A': 'Influenza_A', 'Influenza B': 'Influenza_B',
              'KI polyomavirus Stockholm 60': 'KI_polyomavirus_Stockholm_60', 'WU Polyomavirus': 'WU_Polyomavirus',
              'SARS-CoV-2': 'SARS-CoV-2'
              }


# for sum by groups
norm_counts_groups = {'Adenovirus': ['Human_adenovirus_B1', 'Human_adenovirus_C', 'Human_adenovirus_E'],
                      'Bocavirus': ['Human_bocavirus_2c_PK_isolate_PK-5510', 'Human_bocavirus_3', 'Human_bocavirus_4_NI_strain_HBoV4-NI-385', 'Primate_bocaparvovirus_1_isolate_st2'],
                      'Coronavirus': ['Human_coronavirus_229E', 'Human_coronavirus_HKU1', 'Human_Coronavirus_NL63', 'Human_coronavirus_OC43'],
                      'Enterovirus': ['Enterovirus_C104', 'Human_enterovirus_109'],
                      'Metapneumovirus': ['Human_metapneumovirus'],
                      'Parainfluenza': ['Human_parainfluenza_virus_1', 'Human_parainfluenza_virus_3', 'Human_parainfluenza_virus_4a'],
                      'Parechovirus': ['Human_parechovirus_6', 'Human_parechovirus_type_1_PicoBank/HPeV1/a'],
                      'RSV': ['Human_Respiratory_syncytial_virus_9320', 'Respiratory_syncytial_virus'],
                      'Rhinovirus': ['Human_rhinovirus_89', 'Human_rhinovirus_C', 'Rhinovirus_B14'],
                      'Rubulavirus': ['Human_rubulavirus_2'],
                      'Influenza': ['Influenza_A', 'Influenza_B'],
                      'Polyomavirus': ['KI_polyomavirus_Stockholm_60', 'WU_Polyomavirus'],
                      'SARS-CoV-2': ['SARS-CoV-2']
                      }

add_col_list = ['Site', 'Date', 'External_ID']


def sort_groups(infile):
    df = pd.read_csv(infile)
    df = df.rename(columns={'Unnamed: 0': 'Virus'})
    df = df.set_index('Virus')
    df = df.T
    df = df.rename(columns=virus_dict)
    df = df[virus_dict.values()]
    return df


def sum_groups(df):
    df0 = pd.DataFrame(index=df.index)
    for i, j in zip(norm_counts_groups.keys(), norm_counts_groups.values()):
        df0[i] = df[j].sum(axis=1)
    df0.index.name = 'Respiratory_Seq_ID'
    return df0


def add_col(df):
    for i in add_col_list:
        df.insert(0, i, '')
    return df


@st.cache_data
def clean_data(df):
    df1 = pd.read_csv('drop_these_i_numbers.csv')
    df1 = df1.set_index('Respiratory_Seq_ID')
    df = df.drop([i for i in df1.index])
    return df


@st.cache_data
def group_by_date(df):
    df = df.reset_index()
    df = df.drop(columns=['Respiratory_Seq_ID', 'External_ID', 'Site'])
    df = df.groupby('Date')
    df = df.mean()
    return df


@st.cache_data
def read_distribution_data_prep(df):
    df = sort_df_data(df)
    df = df.reset_index()
    df = df.drop(columns=['Date'])
    df['Index'] = [i + 1 for i in range(len(df))]
    df = df.set_index('Index')
    df = df.transform(np.sort)
    return df

# @st.cache_data
# def read_distribution_scatter_graph(df, virus, category):
#     df_min = df[virus].min()
#     df_max = df[virus].max()
#     df_median = df[virus].median()
#     df_std = df[virus].std()
#     green_ceil = 0
#     yellow_ceil = 0
#     if df_max != 0:
#         green_ceil = df_median / df_max
#     else:
#         green_ceil = .1

#     if df_max != 0:
#         yellow_ceil = (df_median + (0.5 * df_std)) / df_max
#     else:
#         yellow_ceil = .5

#     p = px.scatter(df[[virus]],
#                    color='value',
#                    color_continuous_scale=[(0.00, '#66bd63'), (green_ceil, '#66bd63'),
#                                            (green_ceil, '#fed976'), (yellow_ceil, '#fed976'),
#                                            (yellow_ceil, '#fb6a4a'), (1.00, '#fb6a4a')],
#                    width=500, height=350,
#                    title=f'{category} {virus} Read Distribution',
#                    labels={'value': 'Reads per Million',
#                            'Index': 'Samples',
#                            'variable': 'Pathogen'
#                    },
#                    template='plotly_dark'
#     )
#     p.update_coloraxes(showscale=False)
#     p.update_yaxes(type='log')
#     return p


@st.cache_data
def read_distribution_scatter_graph(df, virus, category):
    if df[[virus]].max()[0] == 0:
        p = px.scatter(df[[virus]],
                       color='value',
                       color_continuous_scale=[(0.00, '#66bd63'), (0.25, '#66bd63'),
                                               (0.25, '#fed976'), (0.75, '#fed976'),
                                               (0.75, '#fb6a4a'), (1.00, '#fb6a4a')],
                       width=500, height=350,
                       title=f'{category} {virus} Read Distribution',
                       labels={'value': 'Reads per Million',
                               'Index': 'Samples',
                               'variable': 'Pathogen'
                               },
                       template='plotly_dark'
                       )
        p.update_coloraxes(showscale=False)
        p.update_yaxes(type='log')
        return p
    else:
        df_drop_0s = df[virus].loc[~(df[virus] == 0)]
        df_drop_0s = df_drop_0s.reset_index()
        df_drop_0s.index = df_drop_0s.index + 1
        df_drop_0s = df_drop_0s.drop(columns='Index')
        df_max = df_drop_0s.max()[0]
        q1 = df_drop_0s.quantile([0.25])
        q3 = df_drop_0s.quantile([0.75])
        green_ceil = q1[virus].values[0] / df_max
        yellow_ceil = q3[virus].values[0] / df_max
        p = px.scatter(df_drop_0s,
                       color='value',
                       color_continuous_scale=[(0.00, '#66bd63'), (green_ceil, '#66bd63'),
                                               (green_ceil, '#fed976'), (yellow_ceil, '#fed976'),
                                               (yellow_ceil, '#fb6a4a'), (1.00, '#fb6a4a')],
                       # range_color=(df_min, df_max),
                       width=500, height=350,
                       title=f'{category} {virus} Read Distribution',
                       labels={'value': 'Reads per Million',
                               'Index': 'Samples',
                               'variable': 'Pathogen'
                               },
                       template='plotly_dark'
                       )
        p.update_coloraxes(showscale=False)
        p.update_yaxes(type='log')
        return p


@st.cache_data
def RVP_split_data_by_campus(df, *prefix):
    df = df[df['External_ID'].str.startswith(prefix)]
    df = df.set_index('Respiratory_Seq_ID')

    return df


@st.cache_data
def RVP_weekly_counts_data_prep(df):
    df1 = sort_df_data(df).tail(15).copy()
    df1 = df1.reset_index()
    date_list = [i.strftime('%b-%d-%Y') for i in df1['Date']]
    df1['Date'] = date_list
    df1 = df1.set_index('Date')
    df2 = df1.T.copy()
    df2 = sort_data2(df2)
    return df2


@st.cache_data
def RVP_weekly_count_bar_graph(df):
    p = px.bar(df,
               color_discrete_sequence=colors1,
               # color='variable',
               # text='variable', # get feedback
               title='Circulating Viruses in ASU Wastewater',
               labels={
                   'value': 'Reads per Million',
                   'Date': 'Week',
                   'variable': 'Circulating pathogens'},
               template='plotly_dark'
               )

    p.update_layout(
        xaxis=dict(
            tickangle=-45
        )
    )
    return p


@st.cache_data
def RVP_weekly_abundance_bar_graph(df):
    p = px.bar(df,
               x='Week',
               y='%',
               color_discrete_sequence=colors1,
               color='Circulating pathogens',
               title='Circulating Viruses in ASU Wastewater',
               # template='plotly_dark'
               )

    p.update_layout(barmode='relative',
                    xaxis=dict(
                        tickangle=-45,
                        # tick0=0.1,
                        # dtick=0.2
                    ),
                    autosize=True,
                    # width=900,
                    # height=500,
                    )
    return p

# [site: 'ASUT', 'ASUP', 'ASUW', 'ASUDT'] [form: 'bar', 'line] [location: Tempe, Polytechnic, West, Downtown]
# probably deprecate this function since it shows the same data as the stacked bar.


@st.cache_data
def RVP_abundance_line_graph(infile, site, location):
    df = pd.read_csv(infile)
    df = RVP_sort_by_location(df, site)
    df = df.drop(columns=['Respiratory_Seq_ID', 'External_ID', 'Site'])
    df = df.groupby('Date')
    df = df.sum().reset_index()
    df['Date'] = pd.to_datetime(df['Date'], format='%y%m%d').dt.strftime('%b-%d-%Y')
    df = df.set_index('Date').T

    date_list = [i for i in df.columns]
    df1 = pd.DataFrame({
        'Sample collection date': date_list,
        'Adenovirus': df.iloc[0].tolist(),
        'Bocavirus': df.iloc[1].tolist(),
        'Coronavirus': df.iloc[2].tolist(),
        'Enterovirus': df.iloc[3].tolist(),
        'Metapneumovirus': df.iloc[4].tolist(),
        'Parainfluenza': df.iloc[5].tolist(),
        'Parechovirus': df.iloc[6].tolist(),
        'RSV': df.iloc[7].tolist(),
        'Rhinovirus': df.iloc[8].tolist(),
        'Rubulavirus': df.iloc[9].tolist(),
        'Influenza': df.iloc[10].tolist(),
        'Polyomavirus': df.iloc[11].tolist(),
        'SARS-CoV-2': df.iloc[12].tolist(),
    })

    df_melt = df1.melt(id_vars='Sample collection date', var_name='Circulating pathogens', value_name='Amount', value_vars=df1.columns[1:], ignore_index=True)
    df_melt['Normalized abundance (% RPM)'] = df_melt['Amount'] / df_melt.groupby('Sample collection date')['Amount'].transform('sum')

    p = px.line(df_melt,
                x='Sample collection date',
                y='Normalized abundance (% RPM)',
                color_discrete_sequence=colors1,
                color='Circulating pathogens',
                title=f'Circulating Viruses in ASU {location} Wastewater',
                )

    p.update_layout(xaxis=dict(
        tickangle=-45,
        nticks=13,
        ticks='outside',
        showline=True
    ),
        yaxis_range=[0, 1],
        yaxis=dict(
        ticks='outside',
        showline=True
    ),
        font=dict(
        size=10
    ),
        autosize=True
    )
    return p

# [site: 'ASUT', 'ASUP', 'ASUW', 'ASUDT'] [form: 'bar', 'line] [location: Tempe, Polytechnic, West, Downtown]


def RVP_absolute_count_df(infile, site, location):
    df = pd.read_csv(infile)
    df = RVP_sort_by_location(df, site)
    df = df.drop(columns=['Respiratory_Seq_ID', 'External_ID', 'Site'])
    df = df.groupby('Date')
    df = df.sum().reset_index()
    df['Date'] = pd.to_datetime(df['Date'], format='%y%m%d').dt.strftime('%b-%d-%Y')
    df = df.set_index('Date').T

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
    df1 = df1.set_index('Week')
    return df1


def RVP_avg_count_lines(df: pd.DataFrame, switch: bool) -> px.line():
    p = px.line(df,
                color='variable',
                color_discrete_sequence=colors2,
                title='Respiratory Virus Pannel Averaged Pathogen Count',
                labels={'value': 'Average Mapped Reads',
                        'Date': 'Collection Date',
                        'variable': 'Circulating Pathogens'
                        },
                log_y=switch,
                )
    p.update_layout(xaxis=dict(
        tickangle=-45,
        tickmode='auto',
    ),
        autosize=True,
    )
    return p


####__________VSP__________####
def VSP_counts_line_graph(df: pd.DataFrame, location: str) -> px.line():
    p = px.line(df,
                color_discrete_sequence=colors2,
                title=f'ASU {location} Grouped VSP',
                labels={'value': 'Total Mapped Reads',
                        'variable': 'VSP Groups',
                        'Date': 'Collection Week'
                        })
    p.update_layout(xaxis=dict(tickangle=-45),
                    autosize=True
                    )
    return p


####_______VSP__________####
def VSP_counts_line_graph(df: pd.DataFrame, location: str) -> px.line():
    p = px.line(df,
                color_discrete_sequence=colors2,
                title=f'ASU {location} Grouped VSP',
                labels={'value': 'Total Mapped Reads',
                        'variable': 'VSP Groups',
                        'Date': 'Collection Week'
                        })
    p.update_layout(xaxis=dict(tickangle=-45),
                    autosize=True
                    )
    return p


####_________MISC__________####
# # Couldnt figure out how to pass CSS through imported fuctions so this function currently exists at the start of each page.
# def HIGHLIGHTER(x: pd.Series):
#     '''
#     This function changes the color of each cell of the read distribution table based on criteria.
#     '''
#     median = int(round(x.median()))
#     high_bar = median + int(round(0.5 * x.std()))
#     def color_switch(number):
#         color = ''
#         if (number == 0) | (number < median):
#             color = 'green'
#         elif (number >= median) & (number < high_bar):
#             color = 'yellow'
#         else:
#             color = 'red'
#         return color
#     return[f'background-color: {color_switch(number)}' for number in x]
