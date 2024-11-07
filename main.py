import smtplib
from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from pyexpat.errors import messages
from wtforms.fields.numeric import FloatField, IntegerField
from wtforms.validators import DataRequired, NumberRange, email
from wtforms.fields.simple import SubmitField, StringField, URLField, EmailField
import requests
from datetime import datetime
from sqlalchemy import desc

APIKEY = 'b9a47fe57ebbebfa92c6ca9a7eaf11c8'
APITOKEN = 'eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJiOWE0N2ZlNTdlYmJlYmZhOTJjNmNhOWE3ZWFmMTFjOCIsIm5iZiI6MTczMDQ4NzU1Ni43MDc1NzE3LCJzdWIiOiI2NzI0ZjI1Mjc3MWY1Y2IxNDk1NTgxODkiLCJzY29wZXMiOlsiYXBpX3JlYWQiXSwidmVyc2lvbiI6MX0.pjy1yf6xmkLJ7hEQwMfq4lDHndgF-nZhRB2G7y-azes'
# tmdb_url = f'https://api.themoviedb.org/3/search/movie?query=venom&api_key={APIKEY}'
image_poster = 'https:///image.tmdb.org/t/p/original/'

# print(requests.get(tmdb_url).json())

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)

##CREATE DATABASE
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///./movie-portfolio.db"
# Optional: But it will silence the deprecation warning in the console.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


##CREATE TABLE
class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(250), unique=True, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    ranking = db.Column(db.Integer, nullable=True)
    vote = db.Column(db.Integer, nullable=True)
    img_url = db.Column(db.String(250), unique=True, nullable=False)

    # Optional: this will allow each book object to be identified by its title when printed.
    def __repr__(self):
        return self.title
        # return f"<Movie (title='{self.title}', year={self.year}, description='{self.description}', rating={self.rating}, img_url='{self.img_url}')>"

class AboutForm(FlaskForm):
    name = StringField('Name:', validators=[DataRequired()])
    message = StringField('Message:', validators=[DataRequired()])
    email = EmailField('E-Mail:', validators=[DataRequired()])
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
    aboutform = AboutForm()
    if aboutform.validate_on_submit():
        name = aboutform.name.data
        email = aboutform.email.data
        message = aboutform.message.data
        my_email = "drkuntakinte2000@gmail.com"
        password = "spud szmr gnyf otsy"
        mails = ["jmmapunda@gmail.com", ]
        for mail in mails:
            with smtplib.SMTP("smtp.gmail.com") as connection:
                connection.starttls()
                connection.login(user=my_email, password=password)
                connection.sendmail(
                    from_addr=my_email,
                    to_addrs=mail,
                    msg=f"Subject:{email} Motivation\n\nHello i am {name} \nMessage:{message}\n{email}."
                    )
        print(name)


    return render_template("about.html", aboutform=aboutform)

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

#TODO put a delete link to the movie posters back side
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
    # movie_results = []

    if add_form.validate_on_submit():
        print("added")
        with app.app_context():
            try:

                db.create_all()  # Create tables
                print("Database and table creation successful.")

                # Add a new book record
                # new_movie = Movie(title=add_form.title.data, year=add_form.year.data, description=add_form.description.data, rating=add_form.rating.data, ranking=add_form.ranking.data, review=add_form.review.data, img_url=add_form.img_url.data)
                new_movie = f"{Movie(title=add_form.title.data)}".replace(' ', '+')
                print(new_movie)
                # all of the movie code selection should be here to show results in <p> in add.html and be able to select result to save

                tmdb_url = f'https://api.themoviedb.org/3/search/movie?query={new_movie}&api_key={APIKEY}'
                image_poster = f'https://image.tmdb.org/t/p/original/{"#"}'
                results = [requests.get(tmdb_url).json()]
                data = results[0]['results']
                print(len(data))
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
                    # print(movie_results)



                # db.session.add(new_movie)
                # db.session.commit()

                all_movies = db.session.query(Movie.id, Movie.title, Movie.year, Movie.description, Movie.rating, Movie.ranking, Movie.review, Movie.img_url).all()
                print(new_movie)


            except Exception as e:
                db.session.rollback()  # Roll back if there's any error
                print("Failed to add the movie:", e)

    print(movie_results)
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
