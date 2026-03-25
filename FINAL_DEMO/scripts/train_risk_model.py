import psycopg2
import pandas as pd
import numpy as np

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split




# =========================
# 1. LOAD DATA FROM DB
# =========================
def load_data():
    conn = psycopg2.connect(
            host="postgres_airflow",
            port=5432,
            database="fin_etl_db", 
            user="admin",
            password="admin"
        )

    query = """
        SELECT id, credit_score, loan_amount
        FROM public.fin_risk_assessment
        WHERE credit_score IS NOT NULL
          AND loan_amount IS NOT NULL
    """

    df = pd.read_sql(query, conn)

    conn.close()
    df = df.dropna(subset=["credit_score", "loan_amount"])
    return df


# =========================
# 2. CREATE LABEL (FAKE TRAIN)
# =========================
def create_fake_label(df):
    """
    Vì bạn chưa có Risk thật → tạo tạm để train model
    Sau này có label thật thì bỏ đoạn này
    """

    df = df.copy()

    # logic đơn giản:
    # credit_score thấp + loan cao → risk cao
    df["risk_score"] = (
        (700 - df["credit_score"]) * 0.6 +
        (df["loan_amount"] / 10000) * 0.4
    )

    return df


def train_model(df):
    df = df.dropna(subset=["credit_score", "loan_amount", "risk_score"])
    X = df[["credit_score", "loan_amount"]]
    y = df["risk_score"]
    if len(df) == 0:
        raise ValueError("Dữ liệu sau khi lọc Null bị trống! Kiểm tra lại DB.")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = RandomForestRegressor(
        n_estimators=100,
        max_depth=5,
        random_state=42
    )

    model.fit(X_train, y_train)

    return model

def predict(df, model):
    X = df[["credit_score", "loan_amount"]]

    preds = model.predict(X)

    result = pd.DataFrame({
        "id": df["id"],
        "risk_score": preds
    })

    return result


# =========================
# 5. SAVE TO DB
# =========================
def save_to_db(df_result):
    conn = psycopg2.connect(
            host="postgres_airflow",
            port=5432,
            database="fin_etl_db", 
            user="admin",
            password="admin"
        )
    cur = conn.cursor()

    # Tạo bảng nếu chưa có
    cur.execute("""
        CREATE TABLE IF NOT EXISTS fin_risk_ml_result (
            id INT PRIMARY KEY,
            risk_score FLOAT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    # UPSERT (update nếu tồn tại)
    insert_sql = """
        INSERT INTO fin_risk_ml_result (id, risk_score)
        VALUES (%s, %s)
        ON CONFLICT (id)
        DO UPDATE SET
            risk_score = EXCLUDED.risk_score,
            created_at = CURRENT_TIMESTAMP;
    """

    data = list(df_result.itertuples(index=False, name=None))

    cur.executemany(insert_sql, data)

    conn.commit()
    cur.close()
    conn.close()


# =========================
# MAIN
# =========================
def main():
    print("Loading data from DB...")
    df = load_data()

    print("Creating label...")
    df = create_fake_label(df)

    print("Training model...")
    model = train_model(df)

    print("Predicting risk...")
    result = predict(df, model)

    print("Saving to DB...")
    save_to_db(result)

    print("DONE!")


if __name__ == "__main__":
    main()
