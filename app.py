# to make website for movie recommender system
import streamlit as st
import pickle
import pandas as pd
import requests

# tmdb image path
# https://image.tmdb.org/t/p/w500/kqjL17yufvn9OVLyXYpvtyrFfak.jpg
#                                [         poster path          ]
# json viewer
# http://jsonviewer.stack.hu/#http://api.themoviedb.org/3/movie/550?api_key=f16b6d84f95d8ac3d06ae5384823f2e4
# returns json file
# https://api.themoviedb.org/3/movie/550?api_key=f16b6d84f95d8ac3d06ae5384823f2e4
# api provide movie id       |       api key  |


def fetch_poster(movie_id):
    response = requests.get(
        'https://api.themoviedb.org/3/movie/{}?api_key=f16b6d84f95d8ac3d06ae5384823f2e4&language=en-US'.format(
            movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500" + data['poster_path']


def recommend(movie):
    recommended_movies = []
    recommended_movies_poster = []
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_poster.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_poster


movies_dict = pickle.load(open('movies.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity', 'rb'))

# Title display
st.title('Movie Recommender System')

# add a text box for user to enter movie name
# we can type the movie name or select from drop down list
selected_movie_name = st.selectbox(
    'How would you like to get recommended?',
    movies['title'].values)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])
