from app import app
from models import db
from sqlalchemy import text

with app.app_context():
    try:
        db.session.execute(text("ALTER TABLE \"order\" ADD COLUMN dining_option VARCHAR(20) DEFAULT 'DINE_IN'"))
        db.session.execute(text("ALTER TABLE \"order\" ADD COLUMN payment_method VARCHAR(20) DEFAULT 'COUNTER'"))
        db.session.commit()
        print("Columns dining_option and payment_method added successfully")
    except Exception as e:
        print(f"Error: {e}")
