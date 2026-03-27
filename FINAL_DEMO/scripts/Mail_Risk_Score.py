import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from airflow.operators.python import PythonOperator
from airflow.utils.email import send_email # Hàm gửi mail chuẩn của Airflow
from email.mime.multipart import MIMEMultipart
import smtplib
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
def export_and_email_risk_report(**kwargs):
    # --- BƯỚC 1: Lấy dữ liệu (Giả sử lấy từ Postgres/Oracle) ---
    # Trong thực tế bạn dùng PostgresHook hoặc OracleHook để lấy df
    data = {
        'ID': ['CUST-001', 'CUST-002', 'CUST-003', 'CUST-004', 'CUST-005'],
        'risk_score': [0.92, 0.85, 0.78, 0.45, 0.32]
    }
    df = pd.DataFrame(data).sort_values('risk_score', ascending=False)

    # --- BƯỚC 2: Vẽ biểu đồ ---
    plt.figure(figsize=(10, 5))
    ax = sns.barplot(x='risk_score', y='ID', data=df, palette='Reds_r')
    ax.bar_label(ax.containers[0], padding=3)
    plt.title('Daily Risk Score Report - Automated by Airflow')
    
    chart_path = '/opt/airflow/data/daily_risk_chart.png'
    plt.savefig(chart_path)
    plt.close()

    # --- BƯỚC 3: Gửi Email qua smtplib ---
    sender_email = "trunghieu1706201@gmail.com" # Email của bạn
    receiver_email = "trunghieu170601@gmail.com"
    app_password = "yhuv jixe bppf ivdj" # Mật khẩu ứng dụng 16 số (App Password)

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = f"Báo cáo Rủi ro Tự động - {kwargs['ds']}"

    body = "Chào Team, đây là báo cáo rủi ro tự động từ hệ thống ETL."
    msg.attach(MIMEText(body, 'plain'))

    # Đính kèm file ảnh
    with open(chart_path, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f"attachment; filename= risk_chart.png")
        msg.attach(part)

    # Gửi mail
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, app_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error: {e}")
        raise # Đẩy lỗi ra để Airflow báo Failed nếu gửi thất bại

# Trong DAG của bạn:
# send_report_task = PythonOperator(
#     task_id='send_risk_report_email',
#     python_callable=export_and_email_risk_report,
#     provide_context=True,
#     dag=dag
# )

# Thứ tự chạy: ... >> run_ml_risk_data >> send_report_task >> end