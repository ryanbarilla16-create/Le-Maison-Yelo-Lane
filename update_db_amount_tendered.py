from app import app
from models import db
from sqlalchemy import text

with app.app_context():
    try:
        db.session.execute(text('ALTER TABLE "order" ADD COLUMN amount_tendered NUMERIC(10, 2)'))
        db.session.commit()
    except Exception as e:
        print(f"Error 1: {e}")
        db.session.rollback()
    try:
        db.session.execute(text('ALTER TABLE "order" ADD COLUMN change_amount NUMERIC(10, 2)'))
        db.session.commit()
    except Exception as e:
        print(f"Error 2: {e}")
        db.session.rollback()

print("Columns added successfully or already exist.")
