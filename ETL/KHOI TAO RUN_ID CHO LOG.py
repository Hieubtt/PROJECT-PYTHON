import psycopg2
import uuid

# Cấu hình DB
DB_CONFIG = {
    "host": "localhost", # IP 10.14.29.138 
    "port": 5432,
    "database": "dvdrental", # Sử dụng DB dvdrental
    "user": "postgres",
    "password": "admin"
}

# Tạo định danh cho lần chạy này
RUN_ID = f"RUN_{uuid.uuid4().hex[:8]}"
# Hàm hỗ trợ
def log_step(cur, step_name: str, status: str, message: str = None) -> None:
    sql_log = """
        INSERT INTO etl_log(run_id, step_name, status, message)
        VALUES (%s, %s, %s, %s);
    """
    cur.execute(sql_log, (RUN_ID, step_name, status, message))
def fetch_all(cur, sql: str):
    cur.execute(sql)
    return cur.fetchall()
# Khởi tạo connection và tắt autocommit (Bắt buộc cho ETL)
conn = psycopg2.connect(**DB_CONFIG)
conn.autocommit = False 
cur = conn.cursor()
print(f"Connected successfully! RUN_ID for this session: {RUN_ID}")

