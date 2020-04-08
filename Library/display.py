from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'test'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class Course(db.Model):
    __tablename__ = "courses"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True)
    books = db.relationship("Book", backref="course")


class Book(db.Model):
    __tablename__ = "books"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True)
    author_id = db.Column(db.Integer, db.ForeignKey("courses.id"))


@app.route("/", methods=['GET', 'POST'])
def index():
    courses = Course.query.all()
    return render_template('library.html', courses=courses)


if __name__ == '__main__':
    db.drop_all()
    db.create_all()

    au1 = Course(name='MTH')
    au2 = Course(name='ECEN')
    au3 = Course(name='CSCE')

    bk1 = Book(name='Calculus I')
    bk2 = Book(name='Calculus II')
    bk3 = Book(name='Linear Algebra')
    bk4 = Book(name='Circuit Design')
    bk5 = Book(name='Intro to VLSI')
    bk6 = Book(name='Intro To Python')
    bk7 = Book(name='Flask Tutorial')

    au1.books.append(bk1)
    au1.books.append(bk2)
    au1.books.append(bk3)
    au2.books.append(bk4)
    au2.books.append(bk5)
    au3.books.append(bk6)
    au3.books.append(bk7)

    db.session.add_all([au1, au2, au3])
    db.session.add_all([bk1, bk2, bk3, bk4, bk5, bk6, bk7])
    
    db.session.commit()
    app.run(debug=True)
