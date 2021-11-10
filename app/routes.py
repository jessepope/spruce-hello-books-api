from app import db
from app.models.book import Book
from app.models.genre import Genre
from app.models.author import Author
from flask import Blueprint, jsonify, make_response, request

books_bp = Blueprint("books_bp", __name__, url_prefix="/books")
genres_bp = Blueprint("genres", __name__, url_prefix="/genres")
authors_bp = Blueprint("authors", __name__, url_prefix="/authors")

@books_bp.route("", methods=["POST", "GET"])
def handle_books():
    if request.method == "POST":
        request_body = request.get_json()
        if "title" not in request_body or "description" not in request_body:
            return make_response("Invalid Request", 400)

        new_book = Book(
            title=request_body["title"],
            description=request_body["description"]
        )
        db.session.add(new_book)
        db.session.commit()

        return f"Book {new_book.title} created", 201
    elif request.method == "GET":
        books = Book.query.all()
        books_response = []
        for book in books:
            books_response.append(
                {
                    "id": book.id,
                    "title": book.title,
                    "description": book.description
                }
            )
        return jsonify(books_response)

@books_bp.route("/<book_id>", methods=["GET", "PUT", "PATCH", "DELETE"])
def handle_book(book_id):
    book = Book.query.get_or_404(book_id)

    if book is None:
        return make_response(f"Book {book_id} not found", 404)

    if request.method == "GET":

        response_body = book.to_dict()
        return response_body

    elif request.method == "PUT":
        request_body = request.get_json()

        book.title = request_body["title"]
        book.description = request_body["description"]

        db.session.commit()

        return jsonify(f"Book #{book.id} sucessfully updated"), 200

    elif request.method == "PATCH":
        request_body = request.get_json()

        if "title" in request_body:
            book.title = request_body["title"]

        if "description" in request_body:
            book.description = request_body["description"]

        db.session.commit()

        return jsonify(f"Book #{book.id} sucessfully patched"), 200

    elif request.method == "DELETE":
        db.session.delete(book)
        db.session.commit()
        return jsonify(f"Book #{book.id} sucessfully deleted"), 200

@genres_bp.route("", methods=["GET","POST"])
def handle_genres():
    if request.method == "GET":
        genres = Genre.query.all()
        genres_response = []
        for genre in genres:
            genres_response.append({
                "id": genre.id,
                "name": genre.name
                })
        return jsonify(genres_response)
    elif request.method == "POST":
        request_body = request.get_json()

        genre = Genre(name=request_body["name"])

        db.session.add(genre)
        db.session.commit()

        return jsonify(f"Genre {genre.name} was successfully created"), 201

@books_bp.route("/<book_id>/assign_genres", methods=["PATCH"])
def assign_genres(book_id):
    book = Book.query.get(book_id)

    if book is None:
        return make_response(f"Book #{book.id} not found", 404)
    request_body = request.get_json()

    for id in request_body["genres"]:
        book.genres.append(Genre.query.get(id))
    db.session.commit()

    return make_response("Genres successfully added", 200)

        
