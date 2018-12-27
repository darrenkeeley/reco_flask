from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import MovieForm, MovieForm2
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
from reco_engine import get_genres, which_movie

# movies doesn't use index. Instead use movie_id.
# However, top_k_most_similar does use index.
movies = pd.read_csv(r'data/movies_with_lower.csv')
top_k_most_similar = pd.read_csv(r'data/top_k_most_similar.csv')
top_k_most_similar = top_k_most_similar.set_index('0')


@app.route("/")

@app.route("/home", methods=["GET", "POST"])
def home():
	form = MovieForm2()
	return render_template('home.html', form=form)

@app.route("/about")
def about():
    return render_template("about.html")

"""
@app.route("/movie_reco", methods=["GET", "POST"])
def movie_reco():
	if request.method == 'POST':
		the_data = request.form
		the_output=get_genres(the_data['movie_name'], the_data['movie_year']).to_html()
		return render_template('movie_reco.html', the_output=the_output)
"""

@app.route("/movie_reco2", methods=["GET", "POST"])
def movie_reco2():
	if request.method == 'POST':
		the_data = request.form
		indicator, table = which_movie(the_data['movie_name'], movies=movies, top_k_most_similar=top_k_most_similar)
		table = table.to_html()
		form = MovieForm2()
		return render_template('movie_reco2.html', the_output=table, form=form, indicator=indicator)

	else:
		form = MovieForm2()
		return render_template('movie_reco2.html', form=form)

if __name__ == '__main__':
	app.run()