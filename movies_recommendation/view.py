import requests
from django.http import HttpResponse
from django.shortcuts import render
import pandas as pd
import numpy as np
import json
import pickle

movies_list = pickle.load(open(
    'C:/Users/shaik/Desktop/ML_Projects/Movies_Recommendation_System/movie_list.pkl', 'rb'))
similarity = pickle.load(open(
    'C:/Users/shaik/Desktop/ML_Projects/Movies_Recommendation_System/similarity.pkl', 'rb'))
movies = pickle.load(open(
    'C:/Users/shaik/Desktop/ML_Projects/Movies_Recommendation_System/movies.pkl', 'rb'))


def fetch_poster(movie_id):
    response = requests.get(
        'https://api.themoviedb.org/3/movie/{}?api_key=87fd296c918a3a16d3e0198cb9d48e9f'.format(movie_id))
    data = response.json

    return 'https://image.tmdb.org/t/p/original/'+data['poster_path']


movies_df = pd.DataFrame(movies)
movies_df.columns = ['index', 'id', 'title',
                     'genres', 'keywords', 'cast', 'director', 'vote_average', 'vote_count', 'poster']

top_50 =  pickle.load(open(
    'C:/Users/shaik/Desktop/ML_Projects/Movies_Recommendation_System/Top_50.pkl', 'rb'))
movies_json = movies_df.to_json(
    orient='records', date_format='iso', date_unit='s')
top_50_json = top_50.to_json(
    orient='records', date_format='iso', date_unit='s')


with open('top_50.json', 'w') as js_file:
    js_file.write(top_50_json)

with open('top_50.json', 'r', encoding='utf-8') as f:
    try:
        Top_50 = json.load(f)  # 👈️ parse the JSON with load()

        # print(my_data)
    except BaseException as e:
        print('The file contains invalid JSON')


with open('movies.json', 'w') as js_file:
    js_file.write(movies_json)

with open('movies.json', 'r', encoding='utf-8') as f:
    try:
        my_movies = json.load(f)  # 👈️ parse the JSON with load()

        # print(my_data)
    except BaseException as e:
        print('The file contains invalid JSON')


df = pd.DataFrame(movies_list)
df.columns = ['id', 'title', 'tags']


movie_json = df.to_json(orient='records', date_format='iso', date_unit='s')

with open('data.json', 'w') as js_file:
    js_file.write(movie_json)

with open('data.json', 'r', encoding='utf-8') as f:
    try:
        my_data = json.load(f)  # 👈️ parse the JSON with load()

        # print(my_data)
    except BaseException as e:
        print('The file contains invalid JSON')


def home(request):
    data = {
        'movies' : Top_50,
    }
    return render(request, 'home.html', data)


def recommended(request):
    r_data = [
        {
        "title": "STONES FROM THE RIVER",
        "director": ["Ursula Hegi"],
        "genres": ["Action , Drama"],
    },
    ]
    try:
        user_input = request.GET.get('user_input')
        print(user_input)
        index = np.where(movies.title == user_input)[0][0]
        print(index)
        distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
        title = []
        director = []
        genres = []
        cast = []
        poster = []

        for i in distances[0:20]:
            movie_id = movies_df.iloc[i[0]]['id']
            title.append(movies_df.iloc[i[0]]['title'])
            director.append(movies_df.iloc[i[0]]['director'])
            genres.append(movies_df.iloc[i[0]]['genres'])
            poster.append(movies_df.iloc[i[0]]['poster'])


        r_df = pd.DataFrame(list(zip(title, director, genres, poster)),
                            columns=['title', 'director', 'genres', 'poster'])
        
        
        recommend_df = r_df.to_json(
            orient='records', date_format='iso', date_unit='s')
        with open('recommended_data.json', 'w') as js_file:
            js_file.write(recommend_df)
        with open('recommended_data.json', 'r', encoding='utf-8') as f:
            try:
                r_data = json.load(f)  # 👈️ parse the JSON with load()

        # print(my_data)
            except BaseException as e:
                print('The file contains invalid JSON')

    except:
        pass


    return render(request, 'recommendations.html', {'movies': r_data, 'info':'no recommendations found'})


def sub_nav(request):
    return render(request, 'sub_nav.html')