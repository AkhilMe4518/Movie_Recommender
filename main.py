import streamlit as st
import pickle
import pandas as pd
import requests


def getPoster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=b1e10d8862abefe84f4bae03bf2c646b&language=en-US".format(
        movie_id)
    data = requests.get(url)
    data = data.json()
    try:
        poster_path = data['poster_path']
        full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
        return full_path
    except:
        return None


def get_movieid(movie):
    return movie_list[movie_list['title'] == movie].index[0]


def Recommend(movie, top=32):
    index = get_movieid(movie)
    distances = sorted(
        list(enumerate(Recommendation_data[index])), reverse=True, key=lambda x: x[1])
    # for i in distances[:10]:st.write(i)
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[:top]:
        # fetch the movie poster
        movie_id = movie_list.iloc[i[0]].movie_id
        Poster = getPoster(movie_id)
        if Poster:
            recommended_movie_posters.append(Poster)
            recommended_movie_names.append(movie_list.iloc[i[0]].title)

    return list(zip(recommended_movie_names, recommended_movie_posters))


st.title("Movie recommender")
movie_list = pickle.load(open('movie_list.pkl', 'rb'))
Recommendation_data = pickle.load(open('Recommendation.pkl', 'rb'))
movie_list = pd.DataFrame(movie_list)

Movie = st.selectbox(
    'Select Movie',
    movie_list['title'].values)


if st.button('Show Recommendation'):
    Recommendations = Recommend(Movie)
    st.write(Movie)
    st.image(Recommendations[0][1], width=200)
    for i in range(1, 30, 5):
        mv = Recommendations[i:i+5]
        col1, col2, col3, col4, col5 = st.columns(5)
        try:
            with col1:
                st.text(mv[0][0])
                st.image(mv[0][1])
        except:
            break
        try:
            with col2:
                st.text(mv[1][0])
                st.image(mv[1][1])
        except:
            break
        try:
            with col3:
                st.text(mv[2][0])
                st.image(mv[2][1])
        except:
            break
        try:
            with col4:
                st.text(mv[3][0])
                st.image(mv[3][1])
        except:
            break
        try:
            with col5:
                st.text(mv[4][0])
                st.image(mv[4][1])
        except:
            break
