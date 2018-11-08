from flask import Flask, render_template, url_for
from forms import MovieForm
import pandas as pd
from reco_engine import frogger
app = Flask(__name__)

app.config['SECRET_KEY'] = 'any secret string'

frogs = [frogger("frogger!")]

#movie_ratings = pd.read_csv(r'C:/Google Drive/CSUEB/stat694/reco flask/data/movie_ratings.csv')
#movie_info = pd.read_csv(r'C:/Google Drive/CSUEB/stat694/reco flask/data/movie_info.csv')
#movie_genres = pd.read_csv(r'C:/Google Drive/CSUEB/stat694/reco flask/data/movie_genres.csv')
#movie_corr = pd.read_csv(r'C:/Google Drive/CSUEB/stat694/reco flask/data/movie_corr.csv')

@app.route("/")

@app.route("/home")
def home():
    return render_template("home.html", frogs=frogs)

@app.route("/about")
def about():
    return render_template("about.html", title='About')

@app.route("/movie_reco", methods=["GET", "POST"])
def movie_reco():
	form = MovieForm()

	return render_template('movie_reco.html', title="Movie Recommendations", form=form)