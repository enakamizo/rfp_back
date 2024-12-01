from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import mysql.connector
import os

# .env ファイルを読み込む
load_dotenv()

# FastAPIアプリケーションの初期化
app = FastAPI()

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 必要に応じて特定のオリジンを設定
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# データベース接続設定
db_config = {
    "host": os.getenv("MYSQL_HOST"),
    "user": os.getenv("MYSQL_USER"),
    "password": os.getenv("MYSQL_PASSWORD"),
    "database": os.getenv("MYSQL_DATABASE"),
    "ssl_ca": os.getenv("MYSQL_SSL_CA")
}

# データベース接続を取得する関数
def get_db_connection():
    return mysql.connector.connect(**db_config)

# 日付一覧を取得するエンドポイント
@app.get("/get_all_dates")
def get_all_dates():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT DISTINCT date FROM quizzes")
        dates = [row["date"] for row in cursor.fetchall()]
        return {"dates": dates}
    except mysql.connector.Error as e:
        return {"error": str(e)}
    finally:
        cursor.close()
        conn.close()

# 指定された日付のクイズを取得するエンドポイント
@app.get("/get_questions_by_date/{selected_date}")
def get_questions_by_date(selected_date: str):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT id, question_text, options, correct_index, explanation FROM quizzes WHERE date = %s",
            (selected_date,)
        )
        questions = cursor.fetchall()
        # JSON形式のデータをパース
        for question in questions:
            question["options"] = eval(question["options"])
        return questions
    except mysql.connector.Error as e:
        return {"error": str(e)}
    finally:
        cursor.close()
        conn.close()

@app.get("/")
def read_root():
    return {"message": "FastAPI is running! Use /get_all_dates or /get_questions_by_date/{selected_date} for data access."}
