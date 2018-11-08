# %%
import pandas as pd
import numpy as np



ratings = pd.read_csv('C:/Google Drive/CSUEB/stat694/recommendation system example/ml-latest-small/ratings.csv')
movie_info = pd.read_csv('C:/Google Drive/CSUEB/stat694/recommendation system example/ml-latest-small/movies.csv')

# set index of movie_info to be movie_id
movie_info = movie_info.set_index('movieId')

# %%
# Spread
ratings_spread = ratings.pivot(index='userId', columns='movieId', values='rating')

# Remove movies in movie_info that have no ratings in ratings_spread
movie_info = movie_info[movie_info.index.isin(ratings_spread.transpose().index.values)]

# Normalize
ratings2 = ratings_spread.sub(np.nanmean(ratings_spread, axis=1), axis=0).divide(np.nanstd(ratings_spread, axis=1), axis=0) 

# %%
# Correlation matrix, takes a moment
movie_corr = ratings2.corr()

#%%
# One-hot encode genres
# First, split the genre str

movie_info2 = movie_info.copy()
movie_info2['genres'] = movie_info2['genres'].str.split('|')

# Now we can one-hot encode genres
from sklearn.preprocessing import MultiLabelBinarizer
mlb = MultiLabelBinarizer()
movie_info3 = movie_info2.join(pd.DataFrame(mlb.fit_transform(movie_info2.pop('genres')),
                          columns=mlb.classes_,
                          index=movie_info2.index))

# Some movies have no genres. That column can be dropped like this, but perhaps it should be kept.
# movie_info3 = movie_info3.drop('(no genres listed)', axis=1)


# This is matrix of only genres
movie_info4 = movie_info3.iloc[:,1:]

#%%
# Given index of movie of interest, returns indices of all movies that share at least 1 genre with movie of interest'
# Info_matrix is a one-hot encoded genre matrix
def same_genres(MoI, genre_matrix=movie_info4):
    # Get row of genres of MoI
    MoI_genres = genre_matrix[genre_matrix.index==MoI]
    
    # Remove the genres from original matrix that MoI doesn't have
    z_columns = genre_matrix.loc[:, (MoI_genres != 0).any(axis=0)]
    
    # Remove movies from original matrix that share no genres with MoI (remove rows that have all elements == 0)
    z_final = z_columns.loc[(z_columns != 0).any(axis=1)]
    
    return z_final.index

# %%
def find_similar_movies(data=movie_corr, movie=1, threshold=0):
    x = data.index[data[movie] > threshold].tolist()
    x.remove(movie)
    return x

def WR(v, m, R, C):
    return (v/(v+m))*R + m/(v+m)*C


# %%
def recommend_similar(data_matrix, movie_corr, similar_movie_id, movies=movie_info, percentile=.5, reco_length=30, threshold=.50, filter_by_genre=True):
    # Finding the mean rating for all movies across all users, excluding users who didn't rate
    c = data_matrix[data_matrix != 0].mean()
    
    # Counting how many votes each movie got
    vote_count = np.count_nonzero(data_matrix, axis = 0) # axis = 0 means count by column (by movie)
    
    # This is average rating by movie_id
    vote_average = np.true_divide(data_matrix.sum(axis = 0),(data_matrix!=0).sum(axis = 0))
    
    # Adding vote_count and vote_average to the data
    movies['vote_count'] = vote_count
    movies['vote_average'] = vote_average
    
    # m is a number of vote_counts that is the cut of value
    m = movies['vote_count'].quantile(percentile)
    movies = movies[movies['vote_count'] >= m]
    
    # calculating the weighted average score
    score = WR(movies['vote_count'], m, movies['vote_average'], c)
    
    # SettingWithCopyWarning
    movies['score'] = score
    
    # keep only movies that share at least 1 genre with MoI
    if filter_by_genre == True:
        movies = movies.loc[same_genres(MoI=similar_movie_id)]
    
    # find similar movies by user correlation
    similar_movies = find_similar_movies(data=movie_corr, movie=similar_movie_id, threshold=threshold)
    
    # keep only movies that have similar user correlations
    movies = movies[movies.index.isin(similar_movies)]
    
    # sorting values in desc order
    movies = movies.sort_values(by =['score'], ascending=False) 
    
    # recommend first 30 (if there is less than 30 movies it would show all of them in descending order by score)
    movies = movies.head(reco_length)
    return movies




#%%
# 1218 is index of LA Confidential
results = recommend_similar(data_matrix=ratings_spread.fillna(0), movie_corr=movie_corr, similar_movie_id=1218, reco_length=1000)






#%%
### BELOW THIS IS TEST CODE




























































#%%
movie_ratings = ratings_spread.fillna(0)

movie_ratings.to_csv(r'C:/Google Drive/CSUEB/stat694/reco flask/data/movie_ratings.csv')
movie_info.to_csv(r'C:/Google Drive/CSUEB/stat694/reco flask/data/movie_info.csv')
movie_info4.to_csv(r'C:/Google Drive/CSUEB/stat694/reco flask/data/movie_genres.csv')
movie_corr.to_csv(r'C:/Google Drive/CSUEB/stat694/reco flask/data/movie_corr.csv')


#%%
# TEST
frogger = pd.read_csv(r'C:/Google Drive/CSUEB/stat694/reco flask/data/movie_ratings.csv')



