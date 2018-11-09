from flask import Flask, render_template, url_for, request, redirect
from forms import MovieForm
import pandas as pd
from reco_engine import get_genres
app = Flask(__name__)

app.config['SECRET_KEY'] = 'any secret string'

movie_ratings = pd.read_csv(r'C:/Google Drive/CSUEB/stat694/reco_flask/data/movie_ratings.csv')
movie_ratings = movie_ratings.drop(movie_ratings.columns[0], axis=1)
movie_info = pd.read_csv(r'C:/Google Drive/CSUEB/stat694/reco_flask/data/movie_info.csv')
movie_genres = pd.read_csv(r'C:/Google Drive/CSUEB/stat694/reco_flask/data/movie_genres.csv')

@app.route("/")

@app.route("/home", methods=["GET", "POST"])
def home():
	form = MovieForm()
	return render_template('home.html', title="Enter a movie!", form=form)

@app.route("/about")
def about():
    return render_template("about.html", title='About')

@app.route("/movie_reco", methods=["GET", "POST"])
def movie_reco():
	if request.method == 'POST':
		the_data = request.form
		the_output=get_genres(movie_info, the_data['movie_name'], the_data['movie_year']).to_html()
		return render_template('movie_reco.html', title="Movie Recommendations", the_output=the_output)