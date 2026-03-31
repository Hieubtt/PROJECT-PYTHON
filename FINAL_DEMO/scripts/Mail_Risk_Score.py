import matplotlib
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
# Xóa import psycopg2 nếu không dùng trực tiếp để tránh lỗi thư viện
from sqlalchemy import create_engine # ĐÃ SỬA: Bỏ create_all

def export_and_email_risk_report():
    print("--- Bắt đầu tiến trình kết nối Database ---")
    
    # 1. Cấu hình thông tin (Nên ưu tiên dùng os.getenv để bảo mật khi thuyết trình)
    db_user = "admin"
    db_password = "admin"
    db_host = "postgres_airflow" 
    db_port = "5432"
    db_name = "fin_etl_db"

    # 2. Tạo Connection String chuẩn cho SQLAlchemy
    conn_url = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    engine = create_engine(conn_url)

    try:
        # 3. Thực thi truy vấn SQL lấy dữ liệu
        query = "SELECT id, CAST(risk_score AS FLOAT) AS risk_score FROM fin_risk_ml_result"
        print(f"--- Đang thực thi query: {query} ---")
        
        # Dùng engine của SQLAlchemy để đọc SQL trực tiếp vào DataFrame
        df = pd.read_sql(query, engine)
        
        if df.empty:
            print("!!! CẢNH BÁO: Database không có dữ liệu.")
            return

        df = df.sort_values('risk_score', ascending=False).head(10)

    except Exception as e:
        print(f"!!! LỖI KẾT NỐI DATABASE: {e}")
        exit(1)

    # 4. Vẽ biểu đồ
    sns.set_theme(style="whitegrid")
    fig, ax = plt.subplots(figsize=(14, 8)) # Tăng chiều rộng lên 14
    sns.barplot(
        x='risk_score', 
        y='id', 
        data=df, 
        palette='Reds', # Đã sửa: Màu đỏ đậm sẽ dành cho risk_score cao
        hue='id', 
        legend=False,
        ax=ax
    )

    # 3. Thêm số vào đầu cột
    ax.bar_label(ax.containers[0], fmt='%.2f', padding=10, fontweight='bold')

    # 4. TĂNG KHOẢNG TRỐNG BÊN TRÁI ĐỂ HIỆN ID
    # Đây là dòng quan trọng nhất để không bị mất ID
    plt.subplots_adjust(left=0.25) 

    # 5. Tinh chỉnh tiêu đề
    plt.title('BÁO CÁO CHỈ SỐ RỦI RO CHI TIẾT', fontsize=16, pad=20, fontweight='bold')
    plt.xlabel('Điểm rủi ro', fontsize=12)
    plt.ylabel('ID Khách hàng', fontsize=12)
    
    # Giới hạn trục X để không bị mất chữ bên phải
    plt.xlim(0, 1.2) 

    chart_path = '/opt/airflow/data/daily_risk_chart.png'
    os.makedirs(os.path.dirname(chart_path), exist_ok=True)
    plt.savefig(chart_path, dpi=300)
    plt.close()

    # 5. Gửi Email
    sender_email = os.getenv("EMAIL_USER", "trunghieu17062001@gmail.com")
    app_password = os.getenv("EMAIL_APP_PASSWORD", "gylfcildsgleubrk")
    receiver_email = "trunghieu170601@gmail.com"

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = f"Báo cáo Rủi ro Tự động - {pd.Timestamp.now().strftime('%d/%m/%Y')}"

    body = f"Chào Team,\n\nHệ thống đã hoàn tất xử lý ETL. Đã ghi nhận {len(df)} bản ghi mới nhất.\nĐính kèm là biểu đồ phân tích rủi ro thực tế từ Database."
    msg.attach(MIMEText(body, 'plain'))

    try:
        with open(chart_path, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header("Content-Disposition", f"attachment; filename=risk_chart_{pd.Timestamp.now().strftime('%Y%m%d')}.png")
            msg.attach(part)
            
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, app_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
        print("--- EMAIL ĐÃ GỬI THÀNH CÔNG! ---")
    except Exception as e:
        print(f"!!! LỖI GỬI MAIL: {e}")
        exit(1)

if __name__ == "__main__":
    export_and_email_risk_report()