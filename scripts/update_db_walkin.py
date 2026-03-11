"""Add customer_name column to Order table and make user_id nullable for walk-in orders."""
import os
from dotenv import load_dotenv
load_dotenv()

from app import app
from models import db

with app.app_context():
    db.engine.execute("ALTER TABLE \"order\" ALTER COLUMN user_id DROP NOT NULL")
    try:
        db.engine.execute("ALTER TABLE \"order\" ADD COLUMN customer_name VARCHAR(100)")
        print("[OK] Added customer_name column")
    except Exception as e:
        if 'already exists' in str(e).lower() or 'duplicate' in str(e).lower():
            print("[OK] customer_name column already exists")
        else:
            print(f"[!] Error: {e}")
    print("[OK] user_id is now nullable")
    print("Done! Walk-in orders are now supported.")
