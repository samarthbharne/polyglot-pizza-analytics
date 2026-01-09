import pymongo
import psycopg2
import sys

# Replace 'your_password' with the password you created when installing PostgreSQL
POSTGRES_PASSWORD = "1234" 

def test_connections():
    print("--- Starting Connection Test ---")
    
    # 1. Test MongoDB
    try:
        mongo_client = pymongo.MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=2000)
        mongo_client.server_info() # This triggers a real connection attempt
        print("✅ MongoDB Connection: SUCCESS")
    except Exception as e:
        print(f"❌ MongoDB Connection: FAILED. Error: {e}")

    # 2. Test PostgreSQL
    try:
        pg_conn = psycopg2.connect(
            dbname="postgres", 
            user="postgres", 
            password=POSTGRES_PASSWORD, 
            host="localhost",
            port="5432"
        )
        print("✅ PostgreSQL Connection: SUCCESS")
        pg_conn.close()
    except Exception as e:
        print(f"❌ PostgreSQL Connection: FAILED. Error: {e}")

if __name__ == "__main__":
    test_connections()