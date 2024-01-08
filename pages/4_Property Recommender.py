import streamlit as st
import pickle
import pandas as pd
import numpy as np


st.set_page_config(page_title="Recommend Appartments")

st.title(" :red[Property Recommender] ")

with open('location_df1.pkl','rb') as file:
   df = pickle.load(file)


with open('cosine_sim1.pkl','rb') as file:
   cosine_sim1 = pickle.load(file)

with open('cosine_sim2.pkl', 'rb') as file:
    cosine_sim2 = pickle.load(file)

with open('cosine_sim3.pkl', 'rb') as file:
    cosine_sim3 = pickle.load(file)


    def recommend_properties_with_scores(property_name, top_n=5):
        cosine_sim_matrix = 0.5 * cosine_sim1 + 0.8 * cosine_sim2 + 1 * cosine_sim3
        # cosine_sim_matrix = cosine_sim3

        # Get the similarity scores for the property using its name as the index
        sim_scores = list(enumerate(cosine_sim_matrix[df.index.get_loc(property_name)]))

        # Sort properties based on the similarity scores
        sorted_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

        # Get the indices and scores of the top_n most similar properties
        top_indices = [i[0] for i in sorted_scores[1:top_n + 1]]
        top_scores = [i[1] for i in sorted_scores[1:top_n + 1]]

        # Retrieve the names of the top properties using the indices
        top_properties = df.index[top_indices].tolist()

        # Create a dataframe with the results
        recommendations_df = pd.DataFrame({
            'PropertyName': top_properties,
            'SimilarityScore': top_scores
        })

        return recommendations_df





#st.dataframe(df)

#st.title("Select Location and Radius")
st.markdown(" ##  :blue[Select Location and Radius]")


selected_location = st.selectbox('Location',sorted(df.columns.to_list()))

radius = st.number_input('Radius in Kms ')

if st.button('Search'):
    result_ser = df[df[selected_location] < radius*1000][selected_location].sort_values()

    for key,value in result_ser.items():
        st.markdown(f" ###  :green[{key}      --->      {round(value/1000,1)}  kms]")

        #st.text(str(key)+ "    --->    " +str(round(value/1000)) + 'kms')


#st.title('Recommend Appartments')
st.markdown(" ##  :blue[ Appartment Recommendations]")


selected_appartment = st.selectbox('Select an Appartment',sorted(df.index.to_list()))

if st.button('Recommend'):
    recommendation_df = recommend_properties_with_scores(selected_appartment)

    #st.dataframe(recommendation_df)
    x = pd.DataFrame(recommendation_df)
    st.markdown(" ### Recommended Appartments are :")
    for i in x['PropertyName']:
        st.markdown(f" #### :orange[{i}]")
