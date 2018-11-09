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

def get_genres(movie_info, movie_name, movie_year):
	movie_str = f'{movie_name} ({movie_year})'
	return movie_info[movie_info['title']==movie_str]