from flask import Flask, jsonify, request
import pandas as pd
import random
from functools import wraps
from flask_cors import CORS
def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('APIKEY')
        if api_key and api_key == API_KEY:
            return f(*args, **kwargs)
        else:
            return jsonify({"error": "Unauthorized access"}), 401
    return decorated_function
app = Flask(__name__)



# Mock database - Danh sách sách
books = [
    {"id": 1, "title": "Lập trình Python", "author": "Nguyễn Văn A", "year": 2020, "available": True},
    {"id": 2, "title": "Trí tuệ nhân tạo", "author": "Trần Thị B", "year": 2021, "available": True},
    {"id": 3, "title": "Học máy cơ bản", "author": "Lê Văn C", "year": 2019, "available": False},
]

API_KEY = "123"
def check_data(data):
    if not data.get("title") or not isinstance(data.get("year"),int) or not data.get("author"):
        return  "Nhập thiếu dữ liệu , vui lòng nhâp lại"
    return True

def get_next_id():
    if books:
        return max(book["id"] for book in books) + 1
    return 1

@app.route('/')
def home():
    return "Chào mừng đến với Hệ thống Quản lý Thư viện"

@app.route('/book',methods=["GET"])
@require_api_key
def get_book():
    return jsonify(books)

@app.route('/book/<int:book_id>',methods=["GET"])
@require_api_key
def find_book(book_id):
    book = next((s for s in books if book_id == s["id"]),None)
    if book:
        return jsonify(book)
    return jsonify({'error','Không tìm thấy id book'},404)

@app.route('/book/<int:book_id>',methods=["POST"])
@require_api_key
def create_book(book_id):
    '''Thêm sách mới'''
    data = request.json
    new_book = {
        "id" : get_next_id(),
        "title" : data.get("title"),
        "author" : data.get("author"),
        "year" : data.get("year"),
        "available" : data.get("available",True)
        }
    books.append(new_book)
    return jsonify(new_book),201


@app.route('/book/<int:book_id>',methods=["PUT"])
@require_api_key
def update_book(book_id):
    data = request.json
    error = check_data(data)
    if error is True:
        book = next((s for s in books if book_id == s["id"]),None)
        if book:
            book.update({
                "title" : data.get("title",book["title"]),
                "author" : data.get("author",book["author"]),
                "year" : data.get("year",book["year"])
            })
            return (jsonify(book))
        return jsonify({"error":"Không tìm thấy id book"}),404
    else:
        return jsonify({"error":error},404 )
    


@app.route('/book/<int:book_id>',methods=["DELETE"])
@require_api_key
def delete_book(book_id):
    # data = request.json
    book = next((s for s in books if book_id == s["id"]),None)
    if book:
        deleted = books.pop(book_id) # pop clear theo index 
        print(book)
        #books.remove(book) remove theo đối tương vd  book =  {'id': 2, 'title': 'Trí tuệ nhân tạo', 'author': 'Trần Thị B', 'year': 2021, 'available': True}
        return jsonify(
            {
                "messsage": "Đã xoá thành công",
                "deleted" : deleted
            }
        )  ,200
    return jsonify({"error":"Không tìm thấy id book"},404)
if __name__ == '__main__':
    app.run(debug=True, port=8000)
