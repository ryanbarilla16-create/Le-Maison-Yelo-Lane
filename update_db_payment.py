from app import app
from models import db
from sqlalchemy import text

with app.app_context():
    try:
        db.session.execute(text("ALTER TABLE \"order\" ADD COLUMN payment_status VARCHAR(20) DEFAULT 'UNPAID'"))
        db.session.commit()
        print("Column payment_status added successfully")
    except Exception as e:
        print(f"Error: {e}")
