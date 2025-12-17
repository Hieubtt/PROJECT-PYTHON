from flask import Flask, jsonify, render_template
import pandas as pd
import requests


app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    #return "Welcome to the LEC 10!"
    return render_template('index.html')
# Khi sử dụg render_template -> Hệ thống sẽ tự động tìm kiếm file trong thư mục 'templates'

@app.route('/api/students', methods=['GET'])
def get_students():
    # Load the CSV file into a DataFrame
    df = pd.read_csv('./demo_buoi_10/students_dropout_academic_success.csv')
    # Convert the DataFrame to a list of dictionaries
    students_list = df.to_dict(orient='records')
    # Return the list as a JSON response
    return jsonify(students_list)


@app.route("/students")
def students():
    try:
        resp = requests.get("http://127.0.0.1:8080/api/students", timeout=5)
        resp.raise_for_status()
        students = resp.json()      # Expecting a list of dicts
    except Exception as e:
        # Nếu lỗi, cho list rỗng và gửi message sang template
        students = []
        error = str(e)
    else:
        error = None
    return render_template("students.html", students=students, error=error)



if __name__ == '__main__':
    app.run(debug=True, port=8080)
