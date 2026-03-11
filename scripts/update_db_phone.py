from app import app
from models import db
from sqlalchemy import text

def add_phone_column():
    with app.app_context():
        try:
            db.session.execute(text('ALTER TABLE "user" ADD COLUMN phone_number VARCHAR(15);'))
            db.session.commit()
            print("Column added")
        except Exception as e:
            print("Error or column already exists:", e)

if __name__ == '__main__':
    add_phone_column()
