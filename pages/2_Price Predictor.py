import streamlit as st
import pickle
import bz2file as bz2
import pandas as pd
import numpy as np

st.set_page_config(page_title="Price Predictor ",page_icon='💲')


st.title(" :red[Price Predictor] ")

st.image('img5.png',width=350)

data = bz2.BZ2File('pipeline1.pbz2', 'rb')
pipeline = pickle.load(data)

with open('df (1).pkl','rb') as file:
   df = pickle.load(file)

#with open('pipeline (1).pkl','rb') as file:
 #  pipeline = pickle.load(file)


st.header(':blue[Enter your inputs]')

property_type = st.selectbox('Property Type ',['flat','house'])

sector = st.selectbox('Sector',sorted(df['sector'].unique().tolist()))

bedrooms = float(st.selectbox('Number of Bedroom',sorted(df['bedRoom'].unique().tolist())))

bathrooms = float(st.selectbox('Number of Bathrooms',sorted(df['bathroom'].unique().tolist())))

balcony = st.selectbox('Number of Balcony',sorted(df['balcony'].unique().tolist()))

property_age = st.selectbox('Property Age',sorted(df['agePossession'].unique().tolist()))

built_up_area = float(st.number_input('Built Up Area(in sqft)'))

servant_room = float(st.selectbox('Servant Room',sorted(df['servant room'].unique().tolist())))

store_room = float(st.selectbox('Store Room',sorted(df['store room'].unique().tolist())))

furnishing_type = st.selectbox('Furnishing type',sorted(df['furnishing_type'].unique().tolist()))

luxury_category = st.selectbox('Luxury Category',sorted(df['luxury_category'].unique().tolist()))

floor_category = st.selectbox('Floor Category',sorted(df['floor_category'].unique().tolist()))


if st.button('Predict'):

    # form a database
    data = [[property_type, sector, bedrooms, bathrooms, balcony, property_age, built_up_area, servant_room, store_room, furnishing_type, luxury_category, floor_category]]
    columns = ['property_type', 'sector', 'bedRoom', 'bathroom', 'balcony',
               'agePossession', 'built_up_area', 'servant room', 'store room',
               'furnishing_type', 'luxury_category', 'floor_category']

    # Convert to DataFrame
    one_df = pd.DataFrame(data, columns=columns)

    # predict
    base_price = np.expm1(pipeline.predict(one_df))[0]
    low = base_price - 0.24
    high = base_price + 0.24


    # display
    st.markdown("## :green[**The price of the property is between {} Cr and {} Cr**]".format(round(low,2), round(high,2)))