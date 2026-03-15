from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3
from datetime import datetime
import uvicorn

app = FastAPI()

class Fit3Data(BaseModel):
    user_id: int
    heart_rate: int
    sleep_quality: str = "未知"

@app.post("/api/sync_fit3")
async def sync_fit3_data(data: Fit3Data):
    conn = sqlite3.connect('health_app.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO health_logs (user_id, heart_rate, sleep_quality, notes, created_at)
        VALUES (?, ?, ?, '自動同步自 Samsung Galaxy Fit3', ?)
    ''', (data.user_id, data.heart_rate, data.sleep_quality, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()
    return {"status": "success"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
