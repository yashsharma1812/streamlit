import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt


st.set_page_config(page_title="Analytics",page_icon='📊')


new_df = pd.read_csv('data_viz1 (1).csv')

st.title(":red[Analytics Module] 📈📊")

st.image('img3.jpg',width=400,use_column_width='never')


x = new_df[['sector','price','price_per_sqft','built_up_area','latitude','longitude']]

group_df = x.groupby('sector').mean()[['price','price_per_sqft','built_up_area','latitude','longitude']]




st.header(':orange[Sector Price per sqft Geomap]')

fig = px.scatter_mapbox(group_df, lat="latitude", lon="longitude", color="price_per_sqft", size='built_up_area',
                  color_continuous_scale=px.colors.cyclical.IceFire, zoom=10,
                  mapbox_style="open-street-map",width=1200,height=700,hover_name=group_df.index)

st.plotly_chart(fig,use_container_width=True)


st.header(':orange[Area Vs Price]')

property_type = st.selectbox('**Select Property Type**',['flat','house'])

if property_type == 'house':
    fig1 = px.scatter(new_df[new_df['property_type']== 'house'], x="built_up_area", y="price", color="bedRoom", title="Area Vs Price")
    st.plotly_chart(fig1,use_container_width=True)
else:
    fig1 = px.scatter(new_df[new_df['property_type']== 'flat'], x="built_up_area", y="price", color="bedRoom", title="Area Vs Price")
    st.plotly_chart(fig1,use_container_width=True)

st.header(':orange[BHK  Pie Chart]')

sector_operations = new_df['sector'].unique().tolist()
sector_operations.insert(0,'overall')

selected_sector = st.selectbox('**Select Sector**', sector_operations)

if selected_sector == 'overall':
    fig2 = px.pie(new_df, names='bedRoom',color_discrete_sequence=px.colors.sequential.Agsunset)

    st.plotly_chart(fig2,use_container_width=True)
else:
    fig2 = px.pie(new_df[new_df['sector'] == selected_sector], names='bedRoom',color_discrete_sequence=px.colors.sequential.Agsunset)

    st.plotly_chart(fig2, use_container_width=True)

st.header(':orange[Side by Side BHK price comparison]')

fig3 = px.box(new_df[new_df['bedRoom'] <= 4], x='bedRoom', y='price', title='BHK Price Range')

st.plotly_chart(fig3,use_container_width=True)

st.header(':orange[Side by Side Distplot for property type]')

fig4 = plt.figure(figsize=(10,4))
sns.distplot(new_df[new_df['property_type'] == 'house']['price'],label = 'house')
sns.distplot(new_df[new_df['property_type'] == 'flat']['price'],label = 'flat')
plt.legend()
st.pyplot(fig4)

st.header(':orange[Furnishing Type by Category]')

sector_operations_2 = new_df['sector'].unique().tolist()
sector_operations_2.insert(0,'Overall')

selected_sector_2 = st.selectbox('**Select Sector**', sector_operations_2)

code = ''' 0 - Unfurnished
1 - Furnished
2 - semifurnished'''
st.code(code)

if selected_sector_2 == 'Overall':
    fig5 = px.pie(new_df, names='furnishing_type')

    st.plotly_chart(fig5,use_container_width=True)
else:
    fig5 = px.pie(new_df[new_df['sector'] == selected_sector_2], names='furnishing_type')

    st.plotly_chart(fig5, use_container_width=True)