from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError

DB_URL = "postgresql+psycopg2://userdatabase:passworddatabase@postgres.deefthanawat.online:5432/namedatabase"

def check_connection():
    engine = create_engine(DB_URL)
    try:
        engine.connect().close()  # Just try to connect and immediately close
        print("✅ Connection is open")
    except OperationalError as e:
        print("❌ Connection failed:", e)

if __name__ == "__main__":
    check_connection()
