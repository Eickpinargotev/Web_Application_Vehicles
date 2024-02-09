from itertools import groupby
import pandas as pd
import streamlit as st
import numpy as np
import plotly.express as px
df = pd.read_csv('vehicles_us.csv')
# replace null-values with 0 in 'is_4wd'
df['is_4wd'].fillna(0, inplace=True)
# replace null-values with 'unknown' in 'model_year','paint_color' and 'cylinders' columns
df['model_year'] = df['model_year'].fillna(0).astype('int64')
df['cylinders'] = df['cylinders'].fillna(0).astype('int64')
df['paint_color'] = df['paint_color'].fillna('unknown')
# df['paint_color']=df['paint_color'].fillna()
# replace null-values of 'odometer' with the median according to the condition column.
median_by_condition = df.groupby('condition')['odometer'].median()


# This function is responsible for assigning a value to the odometer based on the value in the
# condition column in the same row.


def mbc(x):
    if pd.isnull(x['odometer']):
        return median_by_condition[x['condition']]
    else:
        return x['odometer']


df['odometer'] = df.apply(mbc, axis=1)
# Change values's type of each columns as above mencioned
df = df.astype({'is_4wd': 'bool', 'price': 'int64', 'odometer': 'int64'})
df2 = df.query('model_year!=0').groupby(['model_year',
                                         'transmission'])
df2 = df2.count().reset_index()
df2 = df2.sort_values(by='model_year')
# model_year_count vs transmission
fig = px.bar(x=df2['model_year'],
             y=df2['price'],
             color=df2['transmission'],
             barmode='group',
             labels={'x': 'years', 'y': 'count'},
             title='Vehicles count by year and transmission')
# price vs transmission
fig1 = px.histogram(df, x='price', color='transmission',
                    title="Vehicles's price count by transmission")
# odometer vs price
df_odometer_price = df.query('odometer!=0')
fig2 = px.scatter(x=df_odometer_price['odometer'],
                  y=df_odometer_price['price'],
                  labels={'x': 'odometer', 'y': 'price'},
                  title='Odometer vs price')
# ---------------------------------------APP CODE----------------------------
st.header("Analysis of the 'vehicles_us.csv' Dataset")
st.subheader('Select the chart that you want to see')
col1, col2, col3 = st.columns(3)
with col1:
    bar_button = st.button('Bar chart')  # crear un botón

with col2:
    bar_button1 = st.button('Histogram chart')  # crear un botón

with col3:
    bar_button2 = st.button('Scatter chart')  # crear un botón

if bar_button:
    st.plotly_chart(fig, use_container_width=True)
    st.write('The bar chart has been built')
if bar_button1:
    st.plotly_chart(fig1, use_container_width=True)
    st.write('The histogram chart has been built')
if bar_button2:
    st.plotly_chart(fig2, use_container_width=True)
    st.write('The scatter chart has been built')


st.subheader('Select the columns you want to use to create a bar chart')
axisxselected = st.radio("Select one",
                         ['model_year', 'transmission', 'paint_color', 'fuel'],
                         )
df['model_year'] = df['model_year'].astype('str').replace('0', 'unknown')
aaxisxselected_df = df.groupby(axisxselected).count().reset_index()
axisxselected_fig = px.bar(aaxisxselected_df, x=axisxselected,
                           y='days_listed',
                           labels={'days_listed': 'Vechicles_count'},
                           title='Vehicles count by ' + axisxselected,
                           barmode='group')
st.plotly_chart(axisxselected_fig, use_container_width=True)
