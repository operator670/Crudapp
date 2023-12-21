from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)



db_username = os.environ.get('DATABASE_USERNAME')
db_password = os.environ.get('DATABASE_PASSWORD')
db_name = os.environ.get('DATABASE_NAME')
db_host = os.environ.get('INSTANCE_HOST')  # Set this to your local MySQL host
db_port = os.environ.get('DATABASE_PORT')  # Set this to your local MySQL port



# Use the host IP address or hostname of your local machine
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+mysqldb://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "somethingunique"

db = SQLAlchemy(app)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float)

    def __init__(self, title, author, price):
        self.title = title
        self.author = author
        self.price = price

@app.route('/')
def index():
    books = Book.query.all()
    return render_template('index.html', books=books)

@app.route('/add/', methods =['POST'])
def insert_book():
    if request.method == "POST":
        book = Book(
            title = request.form.get('title'),
            author = request.form.get('author'),
            price = request.form.get('price')
        )
        db.session.add(book)
        db.session.commit()
        flash("Book added successfully")
        return redirect(url_for('index'))


@app.route('/update/', methods = ['POST'])
def update():
    if request.method == "POST":
        my_data = Book.query.get(request.form.get('id'))

        my_data.title = request.form['title']
        my_data.author = request.form['author']
        my_data.price = request.form['price']

        db.session.commit()
        flash("Book is updated")
        return redirect(url_for('index'))

@app.route('/delete/<id>/', methods = ['GET', 'POST'])
def delete(id):
    my_data = Book.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Book is deleted")
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))

