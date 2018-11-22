# %%
import pandas as pd
import numpy as np
from flaskblog import db, Movie


#%%
"""
ImmutableMultiDict([('csrf_token', 'ImRkM2RkZGQyNWM0YjY5ZTIwMzU2MDlmYTBmNDU3MGNlNTYyZWNhMjgi.W-Uyqg.rd-BpOIiYKeg9dacUKYvq3tfbXE'), 
('movie_name', 'a'), 
('movie_year', 'a'), 
('submit', 'Submit')])
"""



#%%

def get_genres(movie_name, movie_year):
	movie_str = f'{movie_name} ({movie_year})'
	x = Movie.query.filter_by(title=movie_str)
	return pd.read_sql(x.statement, x.session.bind)