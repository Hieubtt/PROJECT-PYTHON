import psycopg2
import uuid
#BƯỚC 1
# Cấu hình DB
DB_CONFIG = {
    "host": "localhost", # IP 10.14.29.138 
    "port": 5432,
    "database": "dvdrental", # Sử dụng DB dvdrental
    "user": "postgres",
    "password": "admin"
}
def setup_tables():
    # Câu lệnh DDL tạo bảng etl_log
    # Tip: Luôn có log_id tự tăng và log_time mặc định để dễ truy vết
    sql_create_log = """
    CREATE TABLE IF NOT EXISTS etl_log (
        log_id SERIAL PRIMARY KEY,
        run_id VARCHAR(50) NOT NULL,
        step_name VARCHAR(100) NOT NULL,
        status VARCHAR(20) NOT NULL,
        message TEXT,
        log_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    
    # Câu lệnh DDL tạo bảng warehouse_rental
    # Chú ý: Cần định nghĩa Primary Key để hỗ trợ lệnh ON CONFLICT (Upsert)
    sql_create_warehouse = """
    CREATE TABLE IF NOT EXISTS warehouse_rental (
        rental_id INTEGER PRIMARY KEY,
        rental_date TIMESTAMP NOT NULL,
        inventory_id INTEGER NOT NULL,
        customer_id INTEGER NOT NULL,
        return_date TIMESTAMP,
        loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    
    conn = None
    cur = None
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        
        print("Đang tạo bảng etl_log...")
        cur.execute(sql_create_log)
        
        print("Đang tạo bảng warehouse_rental...")
        cur.execute(sql_create_warehouse)
        
        # Bắt buộc phải commit vì DDL (Create table) cũng là một transaction
        conn.commit()
        print("Khởi tạo các bảng thành công! Hạ tầng đã sẵn sàng cho ETL.")
        
    except Exception as e:
        print(f"Lỗi khi khởi tạo bảng: {e}")
        if conn:
            conn.rollback()
    finally:
        if cur: cur.close()
        if conn: conn.close()
# Chạy hàm khởi tạo
setup_tables()

#BƯỚC 2
# Tạo định danh cho lần chạy này
RUN_ID = f"RUN_{uuid.uuid4().hex[:8]}"
# Hàm hỗ trợ
def log_step(cur, step_name: str, status: str, message: str = None) -> None:
    sql_log = """R
        INSERT INTO etl_log(run_id, step_name, status, message)
        VALUES (%s, %s, %s, %s);
    """
    cur.execute(sql_log, (RUN_ID, step_name, status, message))
def fetch_all(cur, sql: str):
    cur.execute(sql)
    return cur.fetchall()
# Khởi tạo connection và tắt autocommit (Bắt buộc cho ETL)
conn = psycopg2.connect(**DB_CONFIG)
conn.autocommit = False  # KHI INSERT DỮ LIỆU THÌ LUÔN LUÔN PHẢI AUTOCOMMIT = FALSE ĐỂ GHI NHẬN NẾU CÓ LỖI THÌ KO COMMIT VÀO DATABASE TRÁNH TRƯỜNG HỢP INSERT SAI DỮ LIỆU
cur = conn.cursor()
print(f"Connected successfully! RUN_ID for this session: {RUN_ID}")

#BƯỚC 3

try:
    log_step(cur, "PIPELINE", "START", "Begin ETL run")
    log_step(cur, "LOAD_WAREHOUSE", "START", "Upsert cleaned data into warehouse_rental")
    # Transform & Load kết hợp bằng CTE
    sql_load = """
        WITH cleaned AS (
            SELECT DISTINCT ON (rental_id)
                rental_id, rental_date, inventory_id, customer_id, return_date
            FROM rental
            WHERE customer_id IS NOT NULL 
                AND rental_date IS NOT NULL
            ORDER BY rental_id
        )
        INSERT INTO warehouse_rental(rental_id, rental_date, inventory_id, customer_id, return_date)
        SELECT rental_id, rental_date, inventory_id, customer_id, return_date
        FROM cleaned
        ON CONFLICT (rental_id) DO UPDATE
        SET return_date = EXCLUDED.return_date,
            loaded_at = NOW();
    """
    cur.execute(sql_load)

    #ON CONFLICT (rental_id) DO UPDATE dùng để khi insert vào rental_id đã có rồi thì sẽ tự động cập nhật các cột của rental_id
    # và update lại time cập nhật mới nhất

    log_step(cur, "LOAD_WAREHOUSE", "SUCCESS", "Upsert completed")
    print("Load step executed. BUT not committed yet!")
    #BƯỚC 4
    # 1. Check Missing
    log_step(cur, "VALIDATION_MISSING", "START", "Check missing rental_id")
    sql_val_missing = """
        SELECT rental_id FROM rental WHERE customer_id IS NOT NULL
        EXCEPT
        SELECT rental_id FROM warehouse_rental; --SCIPRT CHECK MISSING DỮ LIỆU TABLE WAREHOUSE VỚI TABLE GỐC
    """
    
    missing = fetch_all(cur, sql_val_missing)
    if len(missing) > 0:
        raise RuntimeError(f"Validation failed: missing {len(missing)} rental_ids.")
    log_step(cur, "VALIDATION_MISSING", "SUCCESS", "No missing data")
    # 2. Check Duplicates
    log_step(cur, "VALIDATION_DUPLICATE", "START", "Check duplicate PK")
    sql_val_dup = """
        SELECT rental_id, COUNT(*) 
        FROM warehouse_rental 
        GROUP BY rental_id HAVING COUNT(*) > 1;
    """
    dup = fetch_all(cur, sql_val_dup)
    if len(dup) > 0:
        raise RuntimeError(f"Validation failed: found duplicates.")
    log_step(cur, "VALIDATION_DUPLICATE", "SUCCESS", "No duplicates")
    print("Validation passed!")

    #BƯỚC 5 (Commit or Rollback)

    # Nếu chạy đến đây tức là không có Exception nào được raise
    log_step(cur, "PIPELINE", "SUCCESS", "ETL completed successfully")
    conn.commit()
    print("PIPELINE PASSED & COMMITTED!")
except Exception as e: # NẾU CÓ MỘT LỖI Ở RUN_ID NÀO THÌ SẼ LẬP TỨC ROLLBACK LẠI VÀ CON TRỎ NHẢY AUTOCOMIT = TRUE 
    # Nếu có lỗi ở BẤT KỲ bước nào phía trên, nhảy vào đây
    conn.rollback() # Trả DB về nguyên trạng
    print(f"PIPELINE FAILED & ROLLED BACK! Error: {e}")
    # Bật lại autocommit chỉ để ghi log thất bại
    conn.autocommit = True
    log_step(cur, "PIPELINE", "FAIL", str(e))

