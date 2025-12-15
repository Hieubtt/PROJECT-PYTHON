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


def normalize_text_str_only(text: str) -> str:
    # Chuyển về chữ thường (casefold chuẩn hơn lower khi xử lý Unicode)
    text = text.casefold()

    # Bỏ khoảng trắng thừa (giữ một khoảng trắng giữa các từ)
    text = ' '.join(text.split()).strip()

    # Bảng ánh xạ các ký tự có dấu tiếng Việt sang không dấu
    mapping = str.maketrans({
        # Chữ a
        'à':'a','á':'a','ả':'a','ã':'a','ạ':'a',
        'ă':'a','ằ':'a','ắ':'a','ẳ':'a','ẵ':'a','ặ':'a',
        'â':'a','ầ':'a','ấ':'a','ẩ':'a','ẫ':'a','ậ':'a',
        'À':'a','Á':'a','Ả':'a','Ã':'a','Ạ':'a',
        'Ă':'a','Ằ':'a','Ắ':'a','Ẳ':'a','Ẵ':'a','Ặ':'a',
        'Â':'a','Ầ':'a','Ấ':'a','Ẩ':'a','Ẫ':'a','Ậ':'a',

        # Chữ e
        'è':'e','é':'e','ẻ':'e','ẽ':'e','ẹ':'e',
        'ê':'e','ề':'e','ế':'e','ể':'e','ễ':'e','ệ':'e',
        'È':'e','É':'e','Ẻ':'e','Ẽ':'e','Ẹ':'e',
        'Ê':'e','Ề':'e','Ế':'e','Ể':'e','Ễ':'e','Ệ':'e',

        # Chữ i
        'ì':'i','í':'i','ỉ':'i','ĩ':'i','ị':'i',
        'Ì':'i','Í':'i','Ỉ':'i','Ĩ':'i','Ị':'i',

        # Chữ o
        'ò':'o','ó':'o','ỏ':'o','õ':'o','ọ':'o',
        'ô':'o','ồ':'o','ố':'o','ổ':'o','ỗ':'o','ộ':'o',
        'ơ':'o','ờ':'o','ớ':'o','ở':'o','ỡ':'o','ợ':'o',
        'Ò':'o','Ó':'o','Ỏ':'o','Õ':'o','Ọ':'o',
        'Ô':'o','Ồ':'o','Ố':'o','Ổ':'o','Ỗ':'o','Ộ':'o',
        'Ơ':'o','Ờ':'o','Ớ':'o','Ở':'o','Ỡ':'o','Ợ':'o',

        # Chữ u
        'ù':'u','ú':'u','ủ':'u','ũ':'u','ụ':'u',
        'ư':'u','ừ':'u','ứ':'u','ử':'u','ữ':'u','ự':'u',
        'Ù':'u','Ú':'u','Ủ':'u','Ũ':'u','Ụ':'u',
        'Ư':'u','Ừ':'u','Ứ':'u','Ử':'u','Ữ':'u','Ự':'u',

        # Chữ y
        'ỳ':'y','ý':'y','ỷ':'y','ỹ':'y','ỵ':'y',
        'Ỳ':'y','Ý':'y','Ỷ':'y','Ỹ':'y','Ỵ':'y',

        # Chữ đ
        'đ':'d','Đ':'d',
    })

    # Bỏ dấu theo bảng ánh xạ
    text = text.translate(mapping)

    return text


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


'''Tìm kiếm danh sách'''
@app.route('/book/search',methods=["GET"])
@require_api_key
def find_book_parameter():
    '''Tìm sách '''
    author = request.args.get("author")
    title = request.args.get("title")
    year = request.args.get("year",type=int)
    id = request.args.get("id",type=int)
    
    result = None
    if author:
        result = next((s for s in books if normalize_text_str_only(s["author"].lower().strip()) == normalize_text_str_only(author.lower().strip())),None)
    elif title:
        result = next((s for s in books if normalize_text_str_only(s["title"].lower().strip()) == normalize_text_str_only(author.lower().strip())),None)
    elif year:
        result = next((s for s in books if s["year"] == year),None)
    elif id:
        result = next((s for s in books if s["id"] == id),None)
    print(result)
    if result:
        return jsonify(result)
        
    else:
        return jsonify({"errror":"Không tìm thấy sách bạn cần tìm"}),404
        #print(author.lower())


'''Tìm kiếm danh sách có nhiều paramters''' # đẩy parameter nếu cùng 1 key mà nhiều lần sẽ đẩy vào mảng list để chạy lọc lấy nhiều values
@app.route('/book/search_parameters',methods=["GET"])
@require_api_key
def find_book_parameters():
    '''Tìm sách'''
    author = request.args.getlist("author")
    title = request.args.getlist("title")
    year = request.args.getlist("year",type=int)
    id = request.args.getlist("id",type=int)
    
    result = []
    print("title:", title)
    for s in books:
        flag = True

        if author and normalize_text_str_only(s["author"].lower().strip()) not in (normalize_text_str_only(t.lower().strip()) for t in author ):
            flag = False
        elif title and normalize_text_str_only(s["title"].lower().strip()) not in (normalize_text_str_only(t.lower().strip()) for t in title ):
            flag = False
        elif year and s["year"] not in (t for t in year):
            flag = False
        elif id and s["id"] not in (t for t in id):
            flag = False


        if flag is True:
            result.append(s)
    if result:
         return jsonify(result)   
    return jsonify({"error":"Không tìm thấy sách !"},404)
        #print(author.lower())        
    
@app.route('/books/available',methods=["GET"])
@require_api_key
def get_book_available():
    #book = next((s for s in books if book_id == s["id"]),None)
    #available = True
    result_avaible = [s for s in books if s["available"] is True]
    if result_avaible:
        return jsonify(result_avaible)
    else:
        return jsonify({"error":"Hiện tại tồn kho sách đã hết"}),401  

    # 12312
    
    # books.append(new_book)
if __name__ == '__main__':
    app.run(debug=True, port=8000)
