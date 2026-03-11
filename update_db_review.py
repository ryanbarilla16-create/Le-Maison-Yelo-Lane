import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('NEON_DATABASE_URL')

def update_db():
    conn = psycopg2.connect(DATABASE_URL)
    conn.autocommit = True
    cursor = conn.cursor()

    print("Adding target columns...")
    
    # Try adding order_id
    try:
        cursor.execute('ALTER TABLE review ADD COLUMN order_id INTEGER REFERENCES "order"(id);')
        print("Successfully added order_id to review table.")
    except psycopg2.errors.DuplicateColumn:
        print("order_id column already exists.")
    except Exception as e:
        print(f"Error adding order_id column: {e}")

    cursor.close()
    conn.close()

if __name__ == '__main__':
    update_db()
