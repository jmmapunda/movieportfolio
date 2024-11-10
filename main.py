import os
import smtplib
from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from pyexpat.errors import messages
from wtforms.fields.numeric import FloatField, IntegerField
from wtforms.validators import DataRequired, Email
from wtforms.fields.simple import SubmitField, StringField, EmailField
import requests
from datetime import datetime
from sqlalchemy import desc
from dotenv import load_dotenv
from supabase import create_client, Client


load_dotenv()
APIKEY = os.getenv('APIKEY')
APITOKEN = os.getenv('APITOKEN')
# tmdb_url = f'https://api.themoviedb.org/3/search/movie?query=venom&api_key={APIKEY}'
image_poster = 'https:///image.tmdb.org/t/p/original/'
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
DBPASSW = os.getenv('DBPASSW')

user=os.getenv('user')
host='aws-0-us-east-1.pooler.supabase.com'
port='6543'
dbname='postgres'

# print(requests.get(tmdb_url).json())

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('app')
Bootstrap(app)

##CREATE DATABASE
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{user}:{DBPASSW}@{host}:{port}/{dbname}"
# app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///./movie-portfolio.db"
# Optional: But it will silence the deprecation warning in the console.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


##CREATE TABLE
class Movie(db.Model):
    # __tablename__ = 'movie'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(9000), unique=True, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(9000), unique=True, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    ranking = db.Column(db.Integer, nullable=True)
    vote = db.Column(db.Integer, nullable=True)
    img_url = db.Column(db.String(9000), unique=True, nullable=False)

    # Optional: this will allow each book object to be identified by its title when printed.
    def __repr__(self):
        return self.title
        # return f"<Movie (title='{self.title}', year={self.year}, description='{self.description}', rating={self.rating}, img_url='{self.img_url}')>"

class AboutForm(FlaskForm):
    name = StringField('Name:', validators=[DataRequired()])
    message = StringField('Message:', validators=[DataRequired()])
    email = EmailField('E-Mail:', validators=[DataRequired(), Email()])
    submit = SubmitField('SEND')

class AddMovie(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    # year = IntegerField('Year', validators=[DataRequired()])
    # description = StringField('Description', validators=[DataRequired()])
    # rating = FloatField('Rating', validators=[DataRequired(), NumberRange(min=1, max=10)])
    # ranking = FloatField('Ranking', validators=[DataRequired(), NumberRange(min=1, max=10)])
    # vote = db.Column(db.Integer, nullable=True)
    # img_url = URLField('Image Url', validators=[DataRequired()])
    submit = SubmitField('Search')


@app.route("/")
def home():
    all_movies = db.session.query(Movie.id, Movie.title, Movie.year, Movie.description, Movie.rating, Movie.ranking,
                                  Movie.vote, Movie.img_url).order_by(desc(Movie.ranking)).all()
    return render_template("index.html", all_movies=all_movies)


@app.route("/about", methods=['GET', 'POST'])
def about():
    all_movies = db.session.query(Movie.id, Movie.title, Movie.year, Movie.description, Movie.rating, Movie.ranking,
                                  Movie.vote, Movie.img_url).order_by(desc(Movie.rating)).all()
    aboutform = AboutForm()
    if aboutform.validate_on_submit():
        name = aboutform.name.data
        email = aboutform.email.data
        message = aboutform.message.data
        my_email = os.getenv('my_email')
        password = os.getenv('password')
        mail = os.getenv('mails')

        with smtplib.SMTP("smtp.gmail.com", 587) as connection:
            connection.starttls()
            connection.login(user=my_email, password=password)
            connection.sendmail(
                from_addr=my_email,
                to_addrs=mail,
                msg=f"Subject:{email}\n\nHello i am {name} \nMessage:{message}\n{email}."
                )

        return redirect(url_for('home'))


    return render_template("about.html", aboutform=aboutform, all_movies=all_movies)

@app.route("/allmovie")
def allmovie():
    all_movies = db.session.query(Movie.id, Movie.title, Movie.year, Movie.description, Movie.rating, Movie.ranking,
                                  Movie.vote, Movie.img_url).order_by(desc(Movie.rating)).all()
    return render_template("allmovie.html", all_movies=all_movies)


# @app.route("/edit/<int:movie_id>", methods=['GET', 'POST'])
# def edit(movie_id):
#     movie = Movie.query.get(movie_id)
#     edit_form = AddForm(obj=movie)  # Pre-fill form with movie data
#     if edit_form.validate_on_submit():
#         movie.ranking = edit_form.ranking.data
#         movie.review = edit_form.review.data
#         db.session.commit()
#         return redirect(url_for('home'))
#     return render_template("edit.html", edit_form=edit_form, movie=movie)


@app.route("/delete/<int:movie_id>",)
def delete(movie_id):
    movie_to_delete = Movie.query.get(movie_id)
    if movie_to_delete:
        db.session.delete(movie_to_delete)
        db.session.commit()

    return redirect(url_for('home'))

@app.route("/vote/<int:movie_id>",)
def vote(movie_id):
    movie_to_vote = Movie.query.get(movie_id)
    if movie_to_vote:
        movie_to_vote.ranking += 1
        db.session.commit()

    return redirect(url_for('home'))

movie_results = []
@app.route('/add/<int:id_movie>', methods=['GET'])
def selected_movie(id_movie):

    for movie in movie_results:
        if movie['id'] == id_movie:
            with app.app_context():
                try:
                    db.create_all()
                    movie_added = Movie(
                        id = movie['id'],
                        title = movie['movie_title'],
                        year=datetime.strptime(movie['movie_release_date'], "%Y-%m-%d").year,
                        # year = movie['movie_release_date'],
                        description = movie['movie_description'],
                        rating = movie['movie_rating'],
                        ranking=movie.get('movie_ranking', 0),  # Default ranking
                        vote=movie.get('movie_vote'),
                        img_url = f"{image_poster}{movie['movie_img_url']}".replace('//', '/')
                        )
                    db.session.add(movie_added)
                    db.session.commit()
                    print(f' movie added is: {movie_added}')
                except Exception as e:
                    db.session.rollback()  # Roll back if there's any error
                    print("Failed 1 to add the movie:", e)


            # print(f' movie added is: {movie_added}')

    return redirect(url_for('home'))

@app.route("/add", methods=['GET', 'POST'])
def add():
    add_form = AddMovie()
    movie_results.clear()
    if add_form.validate_on_submit():
        # Add a new book record
        # new_movie = Movie(title=add_form.title.data, year=add_form.year.data, description=add_form.description.data, rating=add_form.rating.data, ranking=add_form.ranking.data, review=add_form.review.data, img_url=add_form.img_url.data)
        new_movie = f"{add_form.title.data}".replace(' ', '+')
        # print(new_movie)
        # all of the movie code selection should be here to show results in <p> in add.html and be able to select result to save

        tmdb_url = f'https://api.themoviedb.org/3/search/movie?query={new_movie}&api_key={APIKEY}'
        # image_poster = f'https://image.tmdb.org/t/p/original/{"#"}'
        results = [requests.get(tmdb_url).json()]
        data = results[0]['results']

        for n in range(0, len(data)):
            movie_title = data[n]['original_title']
            movie_release_date = data[n]['release_date']
            movie_description = data[n]['overview']
            movie_rating = data[n]['vote_average']
            movie_img_url = data[n]['poster_path']
            id_movie = data[n]['id']
            movie_data = {'id' : id_movie, 'movie_title' : movie_title, 'movie_release_date' : movie_release_date, 'movie_description' : movie_description, 'movie_rating' : movie_rating, 'movie_img_url' : movie_img_url}
            movie_results.append(movie_data)
            # movie_results.append(f'{movie_title} - {movie_release_date}')


    return render_template("add.html", form=add_form, movie_results=movie_results)

# with app.app_context():
#     try:
#         db.create_all()  # Create tables
#         print("Database and table creation successful.")

        # Add a new book record
        # new_movie = Movie(
        #     title="Phone Booth",
        #     year=2002,
        #     description="Publicist Stuart Shepard finds himself trapped in a phone booth, pinned down by an extortionist's sniper rifle. Unable to leave or receive outside help, Stuart's negotiation with the caller leads to a jaw-dropping climax.",
        #     rating=7.3,
        #     ranking=10,
        #     review="My favourite character was the caller.",
        #     img_url="https://image.tmdb.org/t/p/w500/tjrX2oWRCM3Tvarz38zlZM7Uc10.jpg")
        # db.session.add(new_movie)
        # db.session.commit()

        # print("New book added successfully!")
        # view all books
        # all_books = db.session.query(Book).all()

        # update details
        # book = Book.query.filter_by(title='Harry Potter 2').first()
        # book_to_update = Book.query.filter_by(title='Harry Porter and the Chamber of Secrets').first()
        # book_to_update.title = "Harry Porter and"
        # db.session.commit()

        # book_id = 1
        # book_to_update = Book.query.get(book_id)
        # book_to_update.title = "Harry Potter and the Goblet of Fire"
        # db.session.commit()

        # delete a book base on the id
        # book_id = 3
        # book_to_delete = Book.query.get(book_id)
        # db.session.delete(book_to_delete)
        # db.session.commit()
    #     all_movies = db.session.query(Movie.id, Movie.title, Movie.year, Movie.description, Movie.rating, Movie.ranking, Movie.review, Movie.img_url).all()
    #     print(all_movies)
    # except Exception as e:
    #     db.session.rollback()  # Roll back if there's any error
    #     print("Failed to add the Movie:", e)


if __name__ == '__main__':
    app.run(debug=True)
