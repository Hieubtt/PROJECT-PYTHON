import os
import sys
import uuid
import pandas as pd
import psycopg2
from psycopg2.extras import execute_batch

RUN_ID = f"RUN_{uuid.uuid4().hex[:8]}"


SQL_NULL_DATA='''
    select credit_score,loan_amount,id from fin_risk_assessment 
    where credit_score IS NULL OR loan_amount IS NULL 
    OR credit_score = 'NaN' OR loan_amount = 'NaN'
'''
SQL_LOG = "INSERT INTO etl_log(run_id, step_name, status, message) VALUES (%s,%s,%s,%s);"

def log(cur, step: str, status: str, msg: str = ""):
    cur.execute(SQL_LOG, (RUN_ID, step, status, msg))
def main():
    try:
        # Kết nối tới database (nên kết nối trực tiếp vào fin_etl_db nếu đã tạo xong)
        conn = psycopg2.connect(
            host="postgres_airflow",
            port=5432,
            database="fin_etl_db", 
            user="admin",
            password="admin"
        )
        
        # 1. Đọc dữ liệu lỗi vào Pandas
        df_errors = pd.read_sql(SQL_NULL_DATA, conn)
        print(f"Số dòng cần xử lý: {len(df_errors)}")

        if len(df_errors) > 0:
            # 2. TRANSFORM: Dùng Pandas để thay thế NaN/None bằng 0
            # fillna(0) sẽ xử lý cả giá trị Null từ DB và NaN của Pandas
            df_errors['credit_score'] = df_errors['credit_score'].fillna(0)
            df_errors['loan_amount'] = df_errors['loan_amount'].fillna(0)
            
            # Nếu dữ liệu đang là chuỗi 'NaN', ta ép về 0
            df_errors.replace('NaN', 0, inplace=True)

            # 3. LOAD (UPDATE): Chuẩn bị dữ liệu để update ngược lại
            # Cấu trúc: (giá trị mới 1, giá trị mới 2, ID để tìm dòng)
            data_to_update = [
                (row['credit_score'], row['loan_amount'], row['id']) 
                for _, row in df_errors.iterrows()
            ]

            SQL_UPDATE = """
                UPDATE fin_risk_assessment 
                SET credit_score = %s, 
                    loan_amount = %s 
                WHERE id = %s
            """

            with conn.cursor() as cur:
                # Sử dụng execute_batch để update hàng loạt cho nhanh
                execute_batch(cur, SQL_UPDATE, data_to_update, page_size=100)
                log(cur, "PIPELINE", "START", "Transform + Clean data")
                print(f"ETL PASSED | RUN_ID={RUN_ID}")
            
        else:
            print("Không có dòng nào bị NULL/NaN.")
        conn.commit()
        print(f"Đã cập nhật thành công {len(df_errors)} dòng về giá trị 0.")
    except Exception as e:
        print(f"Lỗi: {e}")
        if 'conn' in locals():
            conn.rollback()
            print(f"ETL FAILED | RUN_ID={RUN_ID} | ERROR={e}")
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    main()


