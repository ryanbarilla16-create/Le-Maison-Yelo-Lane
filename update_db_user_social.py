import sys
import os

# Ensure the app context is available
from app import app
from models import db
from sqlalchemy import text

if __name__ == '__main__':
    with app.app_context():
        try:
            # Drop NOT NULL constraint on birthday
            db.session.execute(text('ALTER TABLE "user" ALTER COLUMN birthday DROP NOT NULL;'))
            db.session.commit()
            print("Successfully made 'birthday' nullable in user table.")
        except Exception as e:
            db.session.rollback()
            print(f"Notice: 'birthday' might already be nullable or error occurred: {e}")
            
        try:
            # Add profile_picture_url column
            db.session.execute(text('ALTER TABLE "user" ADD COLUMN profile_picture_url VARCHAR(500);'))
            db.session.commit()
            print("Successfully added 'profile_picture_url' column to user table.")
        except Exception as e:
            db.session.rollback()
            print(f"Notice: 'profile_picture_url' might already exist or error occurred: {e}")
            
        print("Database update complete.")
