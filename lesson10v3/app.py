from flask import Flask, jsonify, render_template
import pandas as pd

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/students', methods=['GET'])
def students():
    return render_template('students.html')

@app.route('/analytics', methods=['GET'])
def analytics():
    return render_template('analytics.html')

@app.route('/sales_dashboard', methods=['GET'])
def sales_dashboard():
    return render_template('sales_dashboard_api.html')

@app.route('/sales_report', methods=['GET'])
def sales_report():
    return render_template('sales_report.html')

@app.route('/api/sales_report', methods=['GET'])
def get_salesreport():
    # Load the CSV file into a DataFrame

    columns_needed = [
    'Ngaydathang',          # Số đơn hàng
    'Nhaphanphoi',            # Ngày đặt hàng
    'MasanphamTAC', 
    'Hoadon',         # Tên khách hàng
    'DoanhSo',          # Loại sản phẩm
    'Doanhthu',                 # Doanh thu
    'SanLuongLe',
    'FreeItem'
    # Thêm/bớt cột tùy ý
]
    df = pd.read_csv('./data/DE.csv', encoding='windows-1258')
    try:
        df = df[columns_needed] 
    except KeyError as e:
        return jsonify({"error": f"Cột không tồn tại trong file: {e}"}), 400
    sales_report = df.to_dict(orient='records')
    
    # Return the list as a JSON response
    return jsonify(sales_report)

@app.route('/api/students', methods=['GET'])
def get_students():
    # Load the CSV file into a DataFrame
    df = pd.read_csv('./data/students_dropout_academic_success.csv')
    # Convert the DataFrame to a list of dictionaries
    students_list = df.to_dict(orient='records')
    
    # Return the list as a JSON response
    return jsonify(students_list)

if __name__ == '__main__':
    app.run(debug=True, port=8080)