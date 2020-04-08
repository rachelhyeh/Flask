# -*- coding: utf-8 -*-
"""
Created on Wed Apr  1 14:20:47 2020

@author: rache
"""


from flask import Flask, render_template, url_for, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.secret_key = 'test'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///library.db"
#app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class Course(db.Model):
    __tablename__ = "courses"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False, unique=True)
    books = db.relationship("Book", backref="course")
    
    
class Book(db.Model):
    __tablename__ = "books"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False, unique=True)
    author_id = db.Column(db.Integer, db.ForeignKey("courses.id"))

    
    
@app.route('/', methods=['Get', 'POST'])
def index():
    #courses = Course.query.all()
    #return render_template('book_test.html', courses=courses)
    

    if request.method == 'POST':
        course_name = request.form['course_name']
        book_name = request.form['book_name']
        if not all([course_name, book_name]):
            flash('Missing one of the information!')
            return redirect('/')
        
        try:
            exist_course = Course.query.filter_by(name=course_name).first()
            if exist_course:
                exist_book = Book.query.filter_by(name=book_name).first()
                if exist_book:
                    flash('The book under that course is already exist!')
                    return redirect('/')
                else:
                    new_book = Book(name=book_name)
                    exist_course.books.append(new_book)
                    db.session.add(new_book)
                    db.session.commit()
                    return redirect('/')
            else:
                new_course = Course(name=course_name)
                new_book = Book(name=book_name)
                new_course.books.append(new_book)
                db.session.add_all([new_course, new_book])
                db.session.commit()
                return redirect('/')
        except:
            return 'There was an issue adding your book!'
    else:        
        courses = Course.query.all()
        return render_template('library.html', courses=courses)        
    


# Create new routes for delete
@app.route('/deleteCourse/<int:course_id>')
def deleteCourse(course_id):
    # id is unique for each
    # Get the task by id, if not exist then 404
    course_to_delete = Course.query.get_or_404(course_id)
    
    try:
        db.session.delete(course_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting the course!'             

@app.route('/deleteBook/<int:book_id>')
def deleteBook(book_id):
    # id is unique for each
    # Get the task by id, if not exist then 404
    book_to_delete = Book.query.get_or_404(book_id)
    
    try:
        db.session.delete(book_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting the book!'  
    
    
    

if __name__ == '__main__':
    db.drop_all()
    db.create_all()

    c1 = Course(name='MTH')
    c2 = Course(name='ECEN')
    c3 = Course(name='CSCE')

    b1 = Book(name='Calculus I')
    b2 = Book(name='Calculus II')
    b3 = Book(name='Linear Algebra')
    b4 = Book(name='Circuit Design')
    b5 = Book(name='Intro to VLSI')
    b6 = Book(name='Intro To Python')
    b7 = Book(name='Flask Tutorial')

    c1.books.append(b1)
    c1.books.append(b2)
    c1.books.append(b3)
    c2.books.append(b4)
    c2.books.append(b5)
    c3.books.append(b6)
    c3.books.append(b7)

    db.session.add_all([c1, c2, c3])
    db.session.add_all([b1, b2, b3, b4, b5, b6, b7])
    
    db.session.commit()
    app.run(debug=True)


