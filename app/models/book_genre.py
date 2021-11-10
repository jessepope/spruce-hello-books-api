from app import db

class BookGenre(db.Model):
    __tablename__ = "books_genres" #why isn't the table auto generated at flask db migrate like the others
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))
    genre_id = db.Column(db.Integer, db.ForeignKey('genre.id'))