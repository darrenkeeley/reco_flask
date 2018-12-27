# %%
import pandas as pd
import numpy as np
from main_app import db, Movie, Wr_score, Genres


#%%
"""
ImmutableMultiDict([('csrf_token', 'ImRkM2RkZGQyNWM0YjY5ZTIwMzU2MDlmYTBmNDU3MGNlNTYyZWNhMjgi.W-Uyqg.rd-BpOIiYKeg9dacUKYvq3tfbXE'), 
('movie_name', 'a'), 
('movie_year', 'a'), 
('submit', 'Submit')])
"""



#%%
def same_genres(MoI, genre_matrix):
    # Get row of genres of MoI
    MoI_genres = genre_matrix[genre_matrix.index==MoI]
    
    # Remove the genres from original matrix that MoI doesn't have
    z_columns = genre_matrix.loc[:, (MoI_genres != 0).any(axis=0)]
    
    # Remove movies from original matrix that share no genres with MoI (remove rows that have all elements == 0)
    z_final = z_columns.loc[(z_columns != 0).any(axis=1)]
    
    return z_final.index.tolist()

# genres parameter is genres csv
def get_genres(movie_name, movie_year):
	# Get movieId from name + year
    movie_str = f'{movie_name} ({movie_year})'
    x = Movie.query.filter_by(title=movie_str)
    movieId = pd.read_sql(x.statement, x.session.bind)['movieId'][0]

    # Get movieId's that share at least 1 genre with movie of interest
    genres = Genres.query
    genres = pd.read_sql(genres.statement, genres.session.bind)
    genres = genres.set_index("movieId")
    y = same_genres(movieId, genres)

    # Filter by these returned movieId's
    a = db.session.query(Wr_score, Movie).filter(Wr_score.movieId == Movie.movieId)
    a = pd.read_sql(a.statement, a.session.bind)

    # Remove one of the movieId columns, because the join returns 2.
    # https://stackoverflow.com/questions/20297317/python-dataframe-pandas-drop-column-using-int
    columnNumbers = [x for x in range(a.shape[1])]
    columnNumbers.remove(2)
    a = a.iloc[:, columnNumbers]
    a = a.set_index("movieId")

    # Filter and then sort by score
    a = a.loc[y].sort_values(by =['score'], ascending=False) 

    return a.dropna()











# Marija's
# returns tuple: (indicator, table)
# index must be shown because a table is returned. movie_id is dropped.
def which_movie(movie_title, movies, top_k_most_similar):
    movie_title = movie_title.lower()
    movie_sub = movies[movies.lower_title.str.find(movie_title) != -1]
    n = len(movie_sub.index)

    if n == 0: 
        return (0 , movie_sub.iloc[:,1:3])

    elif n > 1:
        return (2 , movie_sub.iloc[:,1:3])

    else:
        get_movie_id = int(movie_sub.movie_id)
        items_id = top_k_most_similar.iloc[get_movie_id,] # take movies that are most similar with movi_id = item_num
        movie_info_item = movies.copy()
        movie_info_item = movie_info_item.set_index('movie_id')
        return (1, movie_info_item.loc[items_id.astype('int'),:].iloc[:,0:2])