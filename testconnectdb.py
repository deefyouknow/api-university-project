from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
import time

# Hostname ต้องเป็น localhost เพราะเราจะเชื่อมต่อผ่าน cloudflared bridge
# เพิ่ม ?connect_timeout=5 เพื่อควบคุมเวลาสูงสุดที่รอสร้างการเชื่อมต่อ
DB_URL = "postgresql+psycopg2://userdatabase:passworddatabase@dserver.thddns.net:6869/namedatabase"

def check_connection():
    # ลบ connect_args ที่ซ้ำซ้อนออก
    engine = create_engine(DB_URL)
    try:
        print("⏳ Attempting database connection...")
        start_time = time.time()
        # ถ้าไม่มี Bridge รันอยู่ โค้ดจะหยุดค้างไม่เกิน 5 วินาทีแล้วแจ้ง error
        connection = engine.connect()
        connection.close()
        end_time = time.time()
        print("✅ Connection is open (Time: {:.2f}s)".format(end_time - start_time))
    except OperationalError as e:
        print("❌ Connection failed after 5s timeout. (Error:", e, ")")

if __name__ == "__main__":
    check_connection()
