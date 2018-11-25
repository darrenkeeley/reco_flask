from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import MovieForm
import pandas as pd

app = Flask(__name__)

app.config['SECRET_KEY'] = 'any secret string'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)

class Movie(db.Model):
	# title includes year in original data
	movieId = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(120), unique=False, nullable=False)
	genres = db.Column(db.String(120))

	def __repr__(self):
		return f"Movie('{self.movieId}', '{self.title}', '{self.genres}')"

class Wr_score(db.Model):
	movieId = db.Column(db.Integer, primary_key=True)
	score = db.Column(db.Float, unique=False)

	def __repr__(self):
		return f"Wr_score('{self.movieId}', '{self.score}')"

###########################################
class Genres(db.Model):
	movieId = db.Column(db.Integer, primary_key=True)
	no_genres = db.Column(db.Integer, unique=False)
	action = db.Column(db.Integer, unique=False)
	adventure = db.Column(db.Integer, unique=False)
	animation = db.Column(db.Integer, unique=False)
	children = db.Column(db.Integer, unique=False)
	comedy = db.Column(db.Integer, unique=False)
	crime = db.Column(db.Integer, unique=False)
	documentary = db.Column(db.Integer, unique=False)
	drama = db.Column(db.Integer, unique=False)
	fantasy = db.Column(db.Integer, unique=False)
	film_noir = db.Column(db.Integer, unique=False)
	horror = db.Column(db.Integer, unique=False)
	imax = db.Column(db.Integer, unique=False)
	musical = db.Column(db.Integer, unique=False)
	mystery = db.Column(db.Integer, unique=False)
	romance = db.Column(db.Integer, unique=False)
	sci_fi = db.Column(db.Integer, unique=False)
	thriller = db.Column(db.Integer, unique=False)
	war = db.Column(db.Integer, unique=False)
	western = db.Column(db.Integer, unique=False)

	def __repr__(self):
		return f"Genres('{self.movieId}', '{self.no_genres}', '{self.action}', '{self.adventure}', '{self.animation}', \
		'{self.children}', '{self.comedy}', '{self.crime}', '{self.documentary}', '{self.drama}', \
		'{self.fantasy}', '{self.film_noir}', '{self.horror}', '{self.imax}', '{self.musical}', \
		'{self.mystery}', '{self.romance}', '{self.sci_fi}', '{self.thriller}', '{self.war}', '{self.western}')"

# this import must be after db and Movie are defined.
from reco_engine import get_genres

#movie_ratings = pd.read_csv(r'C:/Google Drive/CSUEB/stat694/reco_flask/data/movie_ratings.csv')
#movie_ratings = movie_ratings.drop(movie_ratings.columns[0], axis=1)
#movie_info = pd.read_csv(r'C:/Google Drive/CSUEB/stat694/reco_flask/data/movie_info.csv')
#movie_genres = pd.read_csv(r'C:/Google Drive/CSUEB/stat694/reco_flask/data/movie_genres.csv')
#movie_genres = movie_genres.set_index("movieId")


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
		the_output=get_genres(the_data['movie_name'], the_data['movie_year']).to_html()
		return render_template('movie_reco.html', title="Movie Recommendations", the_output=the_output)

if __name__ == '__main__':
	app.run()