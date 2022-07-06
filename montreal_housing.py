from operator import mul
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.offline as po
import plotly.graph_objects as go
import plotly.graph_objs as pg
import streamlit as st
from millify import millify

st.set_page_config(layout="wide")

df = pd.read_csv('montreal_housing_with_neighborhoods.csv')
data = df.copy()

# Based on the profiling report and considering missing values, the selected variables are:
vars_selected = ['Property_type', 'Area', 'Furnished', 'Lease_term', 'Parking_type', 'Heating', 'Water',
                'Cable', 'Internet', 'Electricity', 'Neighborhood', 'Price']
temp_pdata = data[vars_selected]

# Practical data to use = all rows with price
practical_data = temp_pdata[temp_pdata['Price'].notna()]


# Selecting neighborhoods with at least 7 listings
real_data = practical_data[practical_data.groupby('Neighborhood')['Neighborhood'].transform('size') > 6].reset_index(drop=True)

# Group data by neighborhood, considering the price and property_type
data_grouped = real_data.groupby('Neighborhood')[vars_selected]

# Tuple of group names
group_names = tuple(data_grouped.groups.keys())

st.title('STATISTICS OF 0NE-BEDROOM RENTAL IN MONTREAL BOROUGH USING DATA SCRAPED FROM "RENTALS.CA" ON MAY 20, 2022.')
st.write("")
st.write(' The rentals have been grouped using the postal codes into their respective boroughs. I selected 20 boroughs of interest and present \
    general statistics of the price considering the property type, type of facilities and infrastructure and the utilities available. All prices are \
        in CAD.')

st.write("")
st.subheader("Select the preferred borough")
indicator = st.selectbox('Borough', group_names)

for name, group in data_grouped:

    if indicator == name:
        data = data_grouped.get_group(name)
        apartment_descr = data.Property_type.value_counts().to_dict()
    
        st.write("")
        st.write("")
        l1, l2, l3 = st.columns([1,1,1])
        with l2:
            st.header(name.upper())
        #Print number of listings, most common apartmen type, lease type, and parking
        st.write("")
        st.markdown('**There are {} listings in this borough. These include:**'.format(len(data)))
        for key, val in apartment_descr.items():
            st.write('{} ~ {}'.format(key, val))
        
        st.write("")
        st.write("")
        st.subheader("Let's see the distribution of the prices in this borough and the relationship between the area and the prices to give us a better\
            idea of the price range.")
        col1, col2 = st.columns([1,1])

        with col1:
            hist_plot = px.histogram(data, x='Price', title='Distribution of the prices of 1-bedroom rental in {}'.format(name))
            st.plotly_chart(hist_plot)

        with col2:
            #Nan area values are not plotted
            scat_plot = px.scatter(data, x='Area', y='Price', size='Price', color='Property_type', title=(f'The spread of the prices of 1-bedroom rental with regards to the property area in {name}'))
            st.plotly_chart(scat_plot)

        # Stats
        data_descr = data['Price'].describe()
        min_price = data_descr.loc['min']
        mean_price = data_descr.loc['mean']
        median_price = data_descr.loc['50%']
        max_price = data_descr.loc['max']


        st.write("")
        st.write("")
        st.write("")
        st.subheader('Prices summary')
        fig_dash_min = go.Figure(go.Indicator(
            mode = "gauge+number", value=min_price, title={'text':'Minimum price'},
            domain = {'x':[0,0.5], 'y':[0,0.5]},
            gauge = {'axis': {'range':[min_price-200, max_price+100]},
            'bar': {'color': "darkblue"}}
        ))

        fig_dash_mean = go.Figure(go.Indicator(
            mode = "gauge+number", value=mean_price, title={'text':'Average price'},
            domain = {'x':[0,0.5], 'y':[0,0.5]},
            gauge = {'axis': {'range':[min_price-200, max_price+100]},
            'bar': {'color': "darkblue"}}
        ))

        fig_dash_median = go.Figure(go.Indicator(
            mode = "gauge+number", value=median_price, title={'text':'Median price'},
            domain = {'x':[0,0.5], 'y':[0,0.5]},
            gauge = {'axis': {'range':[min_price-200, max_price+100]},
            'bar': {'color': "darkblue"}}
        ))

        fig_dash_max = go.Figure(go.Indicator(
            mode = "gauge+number", value=max_price, title={'text':'Maximum price'},
            domain = {'x':[0,0.5], 'y':[0,0.5]},
            gauge = {'axis': {'range':[min_price-200, max_price+100]},
            'bar': {'color': "darkblue"}}
        ))

        col3, col4, col5 = st.columns([1,1,1])

        with col3:
            st.plotly_chart(fig_dash_min)

        with col4:
            st.plotly_chart(fig_dash_mean)

        with col5:
            st.plotly_chart(fig_dash_max)


        st.write("")
        st.write("")
        st.write("")
        st.subheader("Let's find out the minimum, average, maximum considering the available utilities.")
    
        options = st.multiselect('Filter by', ['Furnished', 'Heating', 'Electricity',
                                    'Cable', 'Internet', 'Water'], ['Electricity', 'Water'])

        selected = data[(data[options] == 'Yes').all(axis=1)]
        st.write('{} listings found'.format(len(selected)))


        selected_descr = selected['Price'].describe()
        min_sprice = selected_descr.loc['min']
        mean_sprice = selected_descr.loc['mean']
        median_sprice = selected_descr.loc['50%']
        max_sprice = selected_descr.loc['max']

        st.write('Statistics are:')
        col6, col7, col8 = st.columns([1,1,1])

        fig_smin = go.Figure(go.Indicator(
            mode = "number",
            gauge = {'shape': "bullet"},
            value = min_sprice,
            domain = {'x': [0.1, 0.3], 'y': [0.2, 0.2]},
            title = {'text': "Minimum price"}))

        fig_smean = go.Figure(go.Indicator(
            mode = "number",
            gauge = {'shape': "bullet"},
            value = mean_sprice,
            domain = {'x': [0.1, 0.3], 'y': [0.2, 0.2]},
            title = {'text': "Average price"}))

        fig_smax = go.Figure(go.Indicator(
            mode = "number",
            gauge = {'shape': "bullet"},
            value = max_sprice,
            domain = {'x': [0.1, 0.3], 'y': [0.2, 0.2]},
            title = {'text': "Maximum price"}))

        with col6:
            st.plotly_chart(fig_smin)
        with col7:
            st.plotly_chart(fig_smean)
        with col8:
            st.plotly_chart(fig_smax)

        
        st.subheader("Now let's see the data per the utilities selected:")
        with st.expander("Click to see data"):
            st.dataframe(selected)



