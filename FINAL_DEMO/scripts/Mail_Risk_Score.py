import matplotlib
matplotlib.use('Agg') # Bắt buộc phải có dòng này để chạy trong Docker
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os

def export_and_email_risk_report():
    print("--- Bắt đầu tiến trình vẽ biểu đồ ---")
    data = {
        'ID': ['CUST-001', 'CUST-002', 'CUST-003', 'CUST-004', 'CUST-005'],
        'risk_score': [0.92, 0.85, 0.78, 0.45, 0.32]
    }
    df = pd.DataFrame(data).sort_values('risk_score', ascending=False)

    plt.figure(figsize=(10, 5))
    ax = sns.barplot(x='risk_score', y='ID', data=df, palette='Reds_r')
    ax.bar_label(ax.containers[0], padding=3)
    plt.title('Daily Risk Score Report - Automated by Airflow')
    
    # Kiểm tra folder tồn tại trước khi lưu
    chart_path = '/opt/airflow/data/daily_risk_chart.png'
    os.makedirs(os.path.dirname(chart_path), exist_ok=True)
    
    plt.savefig(chart_path)
    plt.close()
    print(f"--- Đã lưu ảnh tại: {chart_path} ---")

    sender_email = os.getenv("EMAIL_USER", "trunghieu170601@gmail.com")
    app_password = os.getenv("EMAIL_APP_PASSWORD", "yhuvjixebppfivdj")
    receiver_email = "trunghieu170601@gmail.com"
   

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = "Báo cáo Rủi ro Tự động - Airflow ETL"

    body = "Chào Team, đây là báo cáo rủi ro tự động từ hệ thống ETL."
    msg.attach(MIMEText(body, 'plain'))

    with open(chart_path, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", "attachment; filename=risk_chart.png")
        msg.attach(part)

    print("--- Đang kết nối Gmail SMTP ---")
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, app_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
        print("--- EMAIL ĐÃ GỬI THÀNH CÔNG! ---")
    except Exception as e:
        print(f"!!! LỖI GỬI MAIL: {e}")
        exit(1) # Thoát với mã lỗi 1 để Airflow báo FAILED

# DÒNG QUAN TRỌNG NHẤT: Gọi hàm để thực thi khi chạy bằng BashOperator
if __name__ == "__main__":
    export_and_email_risk_report()