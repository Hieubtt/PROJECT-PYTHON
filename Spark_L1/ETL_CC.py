from fastapi import FastAPI, BackgroundTasks
import oracledb
from pydantic import BaseModel
from typing import Optional, Dict, Any
import json

app = FastAPI()

# Cấu hình kết nối
DB_CONFIG = {
    "user": "YOUR_USER",
    "password": "YOUR_PASSWORD",
    "dsn": "localhost:1521/orcl"
}

# Hàm thực hiện Insert vào Oracle
def insert_cic_to_db(data: Dict[str, Any]):
    conn = None
    try:
        conn = oracledb.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # Bóc tách dữ liệu từ JSON lồng nhau
        # Dữ liệu chính
        masophieu = data.get("MASOPHIEU")
        ten_sp = data.get("TL001")
        ho_ten = data.get("TL005")
        cccd = data.get("CCCD")
        
        # Dữ liệu từ object BC200 (Nếu không có thì để mặc định là 0)
        bc200 = data.get("BC200", {})
        tong_du_no = bc200.get("BC210", 0)
        so_tctd = bc200.get("BC220", 0)
        du_no_xau = bc200.get("BC250", 0)

        sql = """
            INSERT INTO CIC_REPORTS (
                MASOPHIEU, TEN_SAN_PHAM, TEN_NGUOI_TRA_CUU, SO_CCCD, 
                TONG_DU_NO, SO_TCTD_QUAN_HE, DU_NO_XAU, JSON_FULL
            ) VALUES (:1, :2, :3, :4, :5, :6, :7, :8)
        """
        
        # Lưu toàn bộ json vào cột CLOB để lưu vết
        full_json_str = json.dumps(data, ensure_ascii=False)

        cursor.execute(sql, [
            masophieu, ten_sp, ho_ten, cccd, 
            tong_du_no, so_tctd, du_no_xau, full_json_str
        ])
        
        conn.commit()
        print(f"--> [SUCCESS] Đã lưu phiếu: {masophieu}")

    except Exception as e:
        print(f"--> [ERROR] Lỗi lưu DB: {str(e)}")
    finally:
        if conn:
            conn.close()

# API nhận dữ liệu
@app.post("/api/v1/cic-report")
async def receive_cic_report(payload: Dict[str, Any], background_tasks: BackgroundTasks):
    """
    Nhận JSON báo cáo CIC và lưu vào Oracle.
    """
    # Kiểm tra sơ bộ nếu thiếu mã số phiếu
    if "MASOPHIEU" not in payload:
        return {"status": "error", "message": "Missing MASOPHIEU"}

    # Đẩy vào xử lý ngầm để API phản hồi ngay lập tức
    background_tasks.add_task(insert_cic_to_db, payload)

    return {
        "status": "success",
        "message": f"Đang xử lý phiếu {payload.get('MASOPHIEU')}"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)