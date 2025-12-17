from flask import Flask, jsonify,render_template
import pandas as pd

app = Flask(__name__)
@app.route('/', methods=['GET'])
def home():
    #return "Welcome to the LEC 10!"
    return render_template('index.html')



@app.route('/api/students', methods=['GET'])
def get_students():
    # Load the CSV file into a DataFrame
    df = pd.read_csv('./buoi_10/students_dropout_academic_success.csv')
    # Convert the DataFrame to a list of dictionaries
    students_list = df.to_dict(orient='records')
    
    # Return the list as a JSON response
    return jsonify(students_list)

if __name__ == '__main__':
    app.run(debug=True, port=8080)

