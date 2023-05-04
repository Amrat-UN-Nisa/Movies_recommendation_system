import pickle
import streamlit as st
import requests
import pandas as pd
#this function hit on the API ID
def fetch_poster(movie_id):
    #API KEY Generated from tmdb after login (movies --- getdetail)
    url = "https://api.themoviedb.org/3/movie/{}?api_key=1c438b036f47dd6deea9841d744974e4&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    #tmdb image path https://image.tmdb.org/t/p/w500
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path
#this function recommend the five movies
def movie_recommender(movie):
     movie_index = movies[movies['title'] == movie].index[0]
     #distances = similarity[movie_index]
     movies_list = sorted(list(enumerate(similarity[movie_index])),reverse=True,key = lambda x: x[1])
     recommended_movie_names = []
     recommended_movie_posters = [] 
     for i in movies_list[1:6]:
        #movie_id = i[0] #distances[1:6]: 
        # fetch the movie poster form API
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        #append all the movies name
        recommended_movie_names.append(movies.iloc[i[0]].title)
     return recommended_movie_names,recommended_movie_posters
        
movies_dict = pickle.load(open('movie_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)  #create Dataframe that store the value of new_df dataframe

similarity = pickle.load(open('similarity.pkl','rb'))
st.header("Movies Recommender System")
movie_list = movies['title'].values
#user type 
selected_movie_name = st.selectbox(
    'How would you like to be contacted?',
    (movies['title'].values))

if st.button('Show Recommendation'):
    #function call
    recommended_movie_names,recommended_movie_posters = movie_recommender(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])

    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
        
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])

    st.write('You selected:', selected_movie_name)
