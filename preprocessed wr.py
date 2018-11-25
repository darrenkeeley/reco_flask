#%%
"""
Preprocessed WR
"""



import pandas as pd
import numpy as np

#%%
movie_ratings = pd.read_csv(r'C:/Google Drive/CSUEB/stat694/reco_flask/data/movie_ratings.csv')
movie_ratings = movie_ratings.drop(movie_ratings.columns[0], axis=1)


#%%
# Counting weighted score for selected movies.
# 
# Formula is:
#     
#    $$Weighted Rating (WR) = \frac{v}{v + m}* R + \frac{m}{v + m}*C$$
#    
# *v* - number of votes generated per movie; vote_count
# 
# *m* - minimum number of votes required for the movie to be in the chart (the prerequisite)
# 
# *R* - the mean reating of the movie; vote_average
# 
# *C* - the mean reating of all the movies in the data set

def WR(v, m, R, C):
    return (v/(v+m))*R + m/(v+m)*C


# %%
# data_matrix = movie_ratings as named in flask folder, or ratings_spread as named in original .py
# parameter movies=movie_info
# movie_genres = movie_genres aka movie_info4
    
# Finding the mean rating for all movies across all users, excluding users who didn't rate
c = movie_ratings[movie_ratings != 0].mean().mean()
    
# Counting how many votes each movie got
vote_count = np.count_nonzero(movie_ratings, axis = 0) # axis = 0 means count by column (by movie)
    
# R: This is average rating by movie_id
vote_average = np.true_divide(movie_ratings.sum(axis = 0),(movie_ratings!=0).sum(axis = 0))
    
y = pd.DataFrame(dict(vote_count=vote_count, vote_average=vote_average))

# m is a number of vote_counts that is the cut of value
vote_count2 = pd.DataFrame(vote_count)
m = int(vote_count2.quantile(.5))

x = y[vote_count>m]
    
# calculating the weighted average score
wr_scores = WR(x['vote_count'], m, x['vote_average'], c)

#%%
wr_scores.to_csv(r'C:/Google Drive/CSUEB/stat694/reco_flask/data/wr_scores.csv')

#%%


















































#%%
"""
inserting genres into db
"""

#%%
from flaskblog import db
movie_genres = pd.read_csv(r'C:/Google Drive/CSUEB/stat694/reco_flask/data/movie_genres.csv')

db.create_all()
genres = pd.read_csv(r'C:/Google Drive/CSUEB/stat694/reco_flask/data/movie_genres.csv')
from flaskblog import Genres

for row in genres.iterrows():
	film = Genres(movieId=row[1][0], no_genres=row[1][1], action=row[1][2], adventure=row[1][3], animation=row[1][4], children=row[1][5], comedy=row[1][6], crime=row[1][7], documentary=row[1][8], drama=row[1][9], fantasy=row[1][10], film_noir=row[1][11], horror=row[1][12], imax=row[1][13], musical=row[1][14], mystery=row[1][15], romance=row[1][16], sci_fi=row[1][17], thriller=row[1][18], war=row[1][19], western=row[1][20])
	db.session.add(film)

db.session.commit()