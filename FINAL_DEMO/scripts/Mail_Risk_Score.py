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
        query = "SELECT DISTINCT ON (risk_score) id, risk_score FROM public.fin_risk_ml_result ORDER BY risk_score DESC LIMIT 10"
        print(f"--- Đang thực thi query: {query} ---")
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
    fig, ax = plt.subplots(figsize=(14, 8))

    plot = sns.barplot(
        x='id', 
        y='risk_score', 
        data=df, 
        palette='Reds', 
        hue='id', 
        legend=False,
        ax=ax
    )

    # 5. CÁCH HIỂN THỊ 10 SỐ TRÊN ĐẦU CỘT (Sửa lại phần này)
    # Duyệt qua từng "container" và từng "bar" để dán nhãn chính xác
    for container in ax.containers:
        ax.bar_label(
            container, 
            fmt='%.2f', 
            padding=5, 
            fontweight='bold', 
            fontsize=11,
            color='black'
        )

    # 6. Tinh chỉnh hiển thị
    plt.xticks(rotation=45, ha='right')
    plt.title('BÁO CÁO CHỈ SỐ RỦI RO CHI TIẾT (TOP 10)', fontsize=16, pad=25, fontweight='bold')
    plt.xlabel('ID Khách hàng', fontsize=12, labelpad=10)
    plt.ylabel('Điểm rủi ro', fontsize=12)
    
    # Nới rộng trục Y một chút để con số không bị đè vào lề trên
    max_score = df['risk_score'].max()
    plt.ylim(0, max_score * 1.2) 

    plt.tight_layout()

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