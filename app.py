import streamlit as st
import pickle
import pandas as pd
import requests

# Load data from pickle files
similarity = pickle.load(open('similarity.pkl', 'rb'))
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))

# Convert movie dictionary to a DataFrame
movies = pd.DataFrame(movies_dict)

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    
    recommended_movie_names = []
    recommended_movie_posters = []
    
    for i in distances[1:6]:
        # Fetch the movie poster using the 'id' column from the DataFrame
        movie_id = movies.iloc[i[0]]['id']  
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]]['title'])

    return recommended_movie_names, recommended_movie_posters

# Streamlit App
st.title("'Movie Recommender System'")

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    
    columns = st.columns(5)
    
    for i in range(5):
        with columns[i]:
            st.text(recommended_movie_names[i])
            st.image(recommended_movie_posters[i])
