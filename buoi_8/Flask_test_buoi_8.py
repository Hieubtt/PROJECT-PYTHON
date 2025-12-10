from flask import Flask, render_template, request, redirect, jsonify
import pandas as pd
import random
from functools import wraps

app = Flask(__name__) # Ham khoi tao ung dung Flask
#Mock database
students = [
    {"id": 1, "name": "Phuoc An", "age": 20, "grade": "10A1"},
    {"id": 2, "name": "Tran van A", "age": 20, "grade": "10A2"},    
    {"id": 3, "name": "Tran van B", "age": 20, "grade": "11A1"},   
]
# Get max ID for new student
API_KEY = "123"
def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('APIKEY')
        if api_key and api_key == API_KEY:
            return f(*args, **kwargs)
        else:
            return jsonify({"error": "Unauthorized access"}), 401
    return decorated_function

def check_data(data):
    if not  data.get("name") or not isinstance(data.get("age"),int) or not  data.get("grade") :
        return "Thiếu dữ liệu , vui lòng nhập lại !"
    return True 
def get_next_id():
    if students:
        return max(student["id"] for student in students) + 1
    return 1

@app.route('/') #127.0.0.1:8000/
def home():
    return "Welcome to the Student Management System"

@app.route("/students")
@require_api_key
def get_all_students(): 
    '''Lấy tất cả sinh viên'''
    return jsonify(students)

@app.route("/students/<int:student_id>",methods=['GET'])
def get_student(student_id):
    student = next((s for s in students if student_id==s["id"]),None)
    if student:
        return jsonify(student)
    return jsonify({'error':'Không tìm thấy id học sinh'},404)

@app.route("/students",methods=['POST'])
def add_student():
    data = request.json
    new_student = {
        "id" : get_next_id(),
        "name": data.get("name"),
        "age": data.get("age"),
        "grade": data.get("grade")
    }
    students.append(new_student)
    return jsonify(new_student), 201

@app.route('/students/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    data = request.json

    '''============CHECK DATA============'''
    error = check_data(data)
    if error is not True :
        return ({"error":error},404 )
    else:
        '''============CHECK DATA============'''
        student_update = next((s for s in students if student_id==s["id"]),None)
        if student_update:
            student_update["name"] = data.get("name", student_update["name"])
            student_update["age"] = data.get("age", student_update["age"])
            student_update["grade"] = data.get("grade", student_update["grade"])
            return jsonify(student_update)
        return jsonify({'error':'Không tìm thấy id học sinh'},404)

# print(students) 
if __name__ == '__main__':
    app.run(debug=True, port=8000)