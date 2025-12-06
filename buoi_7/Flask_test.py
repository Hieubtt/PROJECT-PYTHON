from flask import Flask, request, jsonify
import random
import pandas as pd
import os
import json
app = Flask(__name__)
#base = os.path.dirname(__file__)   # thư mục chứa file .py
#path = os.path.join(base, "students_dropout_academic_success.csv")

df = pd.read_csv('./buoi_7/data/students_dropout_academic_success.csv')
df.index.name = 'id'
# Tạo mock dữ liệu học sinh
subjects = ["math", "english", "physics", "chemistry"]
students = [
    {
        "id": i + 1,
        "name": f"Student {i + 1}",
        "scores": {
            subject: round(random.uniform(4.0, 10.0), 1) for subject in subjects
        }
    }
    for i in range(100)
]

# Hàm hỗ trợ lọc điểm
def filter_students(students, filters):
    def compare(value, op, threshold):
        if op == "gte":
            return value >= threshold
        elif op == "lte":
            return value <= threshold
        elif op == "gt":
            return value > threshold
        elif op == "lt":
            return value < threshold
        elif op == "eq":
            return value == threshold
        return True # mặc định nếu không có truy vấn gì thì sẽ trả về True - tức tất cả dữ liệu

    result = []
    for student in students:
        valid = True
        for key, value in filters.items():
            try:
                subject, op = key.split("__")
                score = student["scores"].get(subject)
                if score is None or not compare(score, op, float(value)):
                    valid = False
                    break
            except Exception:
                continue
        if valid:
            result.append(student)
    return result

@app.route('/')
def home():
    return "Hello, Client!"

@app.route('/api/students')
def get_students():
    # request.args se tra ve cac cap key-value vd : [('math__gte': 7 ),('math__ote': 8 )]
    filters = {
        key: value for key, value in request.args.items()
        if "__" in key  # ví dụ: math__gte=7
    }
    filtered_students = filter_students(students, filters)
    return jsonify(filtered_students)

@app.route('/api/get-file')
def get_student_from_file_paramter_id():
    student_id = request.args.get('id')
    try:
        #data = data[data['id']==student_id]
        data = df.to_dict(orient="records")
        student_id = int(student_id)
        student = df.loc[student_id].to_dict()
        return jsonify(student)
    except FileNotFoundError:
        return jsonify({"error":"CSV file not found"}),404
    except Exception as e:
        return jsonify({"error":str(e)}),500  

@app.route('/api/get-file/<int:student_id>')
def get_student_from_file_id(student_id):
    try:
        #data = data[data['id']==student_id]
        data = df.to_dict(orient="records")
        if student_id in df.index:
            return jsonify(df.loc[student_id].to_dict())
    except FileNotFoundError:
        return jsonify({"error":"CSV file not found"}),404
    except Exception as e:
        return jsonify({"error":str(e)}),500    

if __name__ == '__main__':
    app.run(debug=True, port=8080)