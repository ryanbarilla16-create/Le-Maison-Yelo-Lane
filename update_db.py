from app import app
from models import db
from sqlalchemy import text

with app.app_context():
    try:
        db.session.execute(text('ALTER TABLE "order" ADD COLUMN xendit_invoice_id VARCHAR(255)'))
        db.session.commit()
    except Exception as e:
        print(f"Error 1: {e}")
        db.session.rollback()
    try:
        db.session.execute(text('ALTER TABLE "order" ADD COLUMN xendit_invoice_url VARCHAR(255)'))
        db.session.commit()
    except Exception as e:
        print(f"Error 2: {e}")
        db.session.rollback()

print("Columns added successfully or already exist.")
