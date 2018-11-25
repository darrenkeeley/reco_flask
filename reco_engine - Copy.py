# %%
import pandas as pd
import numpy as np


#%%
"""
ImmutableMultiDict([('csrf_token', 'ImRkM2RkZGQyNWM0YjY5ZTIwMzU2MDlmYTBmNDU3MGNlNTYyZWNhMjgi.W-Uyqg.rd-BpOIiYKeg9dacUKYvq3tfbXE'), 
('movie_name', 'a'), 
('movie_year', 'a'), 
('submit', 'Submit')])
"""



#%%

# Given index of movie of interest, returns indices of all movies that share at least 1 genre with movie of interest'
# Info_matrix is a one-hot encoded genre matrix
def same_genres(MoI, genre_matrix):
    # Get row of genres of MoI
    MoI_genres = genre_matrix[genre_matrix.index==MoI]
    
    # Remove the genres from original matrix that MoI doesn't have
    z_columns = genre_matrix.loc[:, (MoI_genres != 0).any(axis=0)]
    
    # Remove movies from original matrix that share no genres with MoI (remove rows that have all elements == 0)
    z_final = z_columns.loc[(z_columns != 0).any(axis=1)]
    
    return z_final.index

# %%
# data_matrix = movie_ratings as named in flask folder, or ratings_spread as named in original .py
# parameter movies=movie_info
# movie_genres = movie_genres aka movie_info4


def reco(movie_name, movie_year):
    movie_str = f'{movie_name} ({movie_year})'
    x = Movie.query.filter_by(title=movie_str)
    return pd.read_sql(x.statement, x.session.bind)


def recommend_similar(data_matrix, similar_movie_id, movies, movie_genres, percentile=.5, reco_length=30, filter_by_genre=True):

    
    # SettingWithCopyWarning
    movies['score'] = score
    
    # keep only movies that share at least 1 genre with MoI
    if filter_by_genre == True:
        movies = movies.loc[same_genres(MoI=similar_movie_id, genre_matrix=movie_genres)]
    
    # sorting values in desc order
    movies = movies.sort_values(by =['score'], ascending=False) 
    
    # recommend first 30 (if there is less than 30 movies it would show all of them in descending order by score)
    movies = movies.head(reco_length)
    return movies






#%%
movie_ratings = pd.read_csv(r'C:/Google Drive/CSUEB/stat694/reco_flask/data/movie_ratings.csv')
movie_ratings = movie_ratings.drop(movie_ratings.columns[0], axis=1)

movie_info = pd.read_csv(r'C:/Google Drive/CSUEB/stat694/reco_flask/data/movie_info.csv')
movie_genres = pd.read_csv(r'C:/Google Drive/CSUEB/stat694/reco_flask/data/movie_genres.csv')

#%%
data_matrix=movie_ratings
similar_movie_id=1
movies=movie_info
movie_genres=movie_genres
percentile=.5
reco_length=30
filter_by_genre=True


#%%



x = recommend_similar(data_matrix=movie_ratings, similar_movie_id=1, movies=movie_info, movie_genres=movie_genres)    




































#%%
def get_genres(movie_info, movie_name):
    return movie_info[movie_info['title']==movie_name]

get_genres(movie_info, "Jumanji (1995)")










