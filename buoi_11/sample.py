from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv, dotenv_values
import os
load_dotenv() 
app = Flask(__name__)
CORS(app)
# Mock data học sinh
students = [
    {"id": 1, "name": "Nguyễn Văn A", "age": 15, "grade": 10, "average_score": 8.5},
    {"id": 2, "name": "Trần Thị B", "age": 16, "grade": 11, "average_score": 9.0},
    {"id": 3, "name": "Lê Văn C", "age": 14, "grade": 9, "average_score": 7.5},
    {"id": 4, "name": "Phạm Thị D", "age": 15, "grade": 10, "average_score": 8.0},
    {"id": 5, "name": "Hoàng Văn E", "age": 16, "grade": 11, "average_score": 8.8},
    {"id": 6, "name": "Đỗ Thị F", "age": 15, "grade": 10, "average_score": 7.8},
    {"id": 7, "name": "Vũ Văn G", "age": 14, "grade": 9, "average_score": 9.2},
    {"id": 8, "name": "Ngô Thị H", "age": 16, "grade": 11, "average_score": 8.3},
    {"id": 9, "name": "Bùi Văn I", "age": 15, "grade": 10, "average_score": 7.9},
    {"id": 10, "name": "Mai Thị K", "age": 14, "grade": 9, "average_score": 8.7}
]


Database_name= os.getenv("Database_name")
User_name=os.getenv("User_name")
Password= os.getenv("Password")

print(Database_name)
print(User_name)
print(Password)

# GET - Lấy danh sách tất cả học sinh
@app.route('/students', methods=['GET'])
def get_students():
    return jsonify(students)

# GET - Lấy thông tin một học sinh theo ID
@app.route('/students/<int:student_id>', methods=['GET'])
def get_student(student_id):
    student = next((student for student in students if student["id"] == student_id), None)
    if student:
        return jsonify(student)
    return jsonify({"message": "Không tìm thấy học sinh"}), 404

# POST - Thêm học sinh mới
@app.route('/students', methods=['POST'])
def add_student():
    new_student = request.get_json()
    if not new_student:
        return jsonify({"message": "Dữ liệu không hợp lệ"}), 400
    
    # Tự động tạo ID mới
    new_id = max(student["id"] for student in students) + 1
    new_student["id"] = new_id
    students.append(new_student)
    return jsonify(new_student), 201

# PUT - Cập nhật thông tin học sinh
@app.route('/students/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    student = next((student for student in students if student["id"] == student_id), None)
    if not student:
        return jsonify({"message": "Không tìm thấy học sinh"}), 404
    
    update_data = request.get_json()
    if not update_data:
        return jsonify({"message": "Dữ liệu không hợp lệ"}), 400
    
    student.update(update_data)
    student["id"] = student_id  # Đảm bảo ID không bị thay đổi
    return jsonify(student)

# DELETE - Xóa học sinh
@app.route('/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    student = next((student for student in students if student["id"] == student_id), None)
    if not student:
        return jsonify({"message": "Không tìm thấy học sinh"}), 404
    
    students.remove(student)
    return jsonify({"message": "Đã xóa học sinh thành công"})

if __name__ == '__main__':
    app.run(debug=True,port=os.getenv("port"))

