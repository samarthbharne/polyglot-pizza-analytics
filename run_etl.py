import pymongo
import psycopg2
import pandas as pd
from datetime import datetime

# CONFIGURATION
POSTGRES_PASSWORD = "1234" # <--- UPDATE THIS
DB_NAME = "pizza_analytics_db"

def run_pipeline():
    print("--- 1. EXTRACT: Connecting to MongoDB ---")
    mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
    # Our data generator saved to 'pizza_analytics_db' in MongoDB
    mongo_db = mongo_client["pizza_analytics_db"]
    raw_logs = list(mongo_db["web_logs"].find())
    
    if not raw_logs:
        print("❌ No logs found in MongoDB. Run generate_logs.py first!")
        return

    print(f"✅ Extracted {len(raw_logs)} logs.")

    print("--- 2. TRANSFORM: Processing Data with Pandas ---")
    df = pd.DataFrame(raw_logs)
    
    # Calculate metrics per user
    # 1. Total clicks (actions)
    # 2. Most viewed pizza (mode of item_name)
    # 3. Last activity time
    summary = df.groupby('user_id').agg(
        total_clicks=('action', 'count'),
        last_active=('timestamp', 'max'),
        favorite_pizza=('item_name', lambda x: x.mode()[0] if not x.mode().empty else "None")
    ).reset_index()
    
    print("✅ Transformation complete. Top insight generated.")

    print("--- 3. LOAD: Moving Data to PostgreSQL ---")
    try:
        # Connect to default 'postgres' first to ensure our DB exists
        conn = psycopg2.connect(dbname="postgres", user="postgres", password=POSTGRES_PASSWORD, host="localhost")
        conn.autocommit = True
        cur = conn.cursor()
        
        # Check if our specific DB exists, if not, create it
        cur.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{DB_NAME}'")
        if not cur.fetchone():
            cur.execute(f"CREATE DATABASE {DB_NAME}")
            print(f"✅ Created Database: {DB_NAME}")
        
        cur.close()
        conn.close()

        # Now connect to the actual project database
        pg_conn = psycopg2.connect(dbname=DB_NAME, user="postgres", password=POSTGRES_PASSWORD, host="localhost")
        pg_cur = pg_conn.cursor()

        # Ensure tables exist
        pg_cur.execute("""
            CREATE TABLE IF NOT EXISTS customers (
                customer_id INT PRIMARY KEY,
                full_name VARCHAR(100)
            );
            CREATE TABLE IF NOT EXISTS user_behavior_metrics (
                user_id INT PRIMARY KEY REFERENCES customers(customer_id),
                total_clicks INT,
                favorite_pizza_viewed VARCHAR(50),
                last_active TIMESTAMP
            );
        """)
        
        # Insert seed customers if table is empty
        pg_cur.execute("SELECT COUNT(*) FROM customers")
        if pg_cur.fetchone()[0] == 0:
            pg_cur.execute("INSERT INTO customers (customer_id, full_name) VALUES (1, 'Alice Smith'), (2, 'Bob Jones')")

        # Upsert the metrics (Update if exists, Insert if new)
        for _, row in summary.iterrows():
            pg_cur.execute("""
                INSERT INTO user_behavior_metrics (user_id, total_clicks, favorite_pizza_viewed, last_active)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (user_id) 
                DO UPDATE SET 
                    total_clicks = EXCLUDED.total_clicks,
                    favorite_pizza_viewed = EXCLUDED.favorite_pizza_viewed,
                    last_active = EXCLUDED.last_active;
            """, (int(row['user_id']), int(row['total_clicks']), row['favorite_pizza'], row['last_active']))

        pg_conn.commit()
        print("✅ LOAD SUCCESS: Data moved to PostgreSQL.")
        
    except Exception as e:
        print(f"❌ SQL Error: {e}")
    finally:
        if 'pg_conn' in locals():
            pg_cur.close()
            pg_conn.close()

if __name__ == "__main__":
    run_pipeline()