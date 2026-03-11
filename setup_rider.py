from app import app
from models import db, User
from sqlalchemy import text
from werkzeug.security import generate_password_hash

with app.app_context():
    # 1. Add delivery columns to order table
    columns = [
        ('delivery_address', 'TEXT'),
        ('delivery_status', 'VARCHAR(20)'),
        ('rider_id', 'INTEGER REFERENCES "user"(id)'),
    ]
    for col_name, col_type in columns:
        try:
            db.session.execute(text(f'ALTER TABLE "order" ADD COLUMN {col_name} {col_type}'))
            db.session.commit()
            print(f"Added column: {col_name}")
        except Exception as e:
            print(f"Column {col_name} already exists or error: {e}")
            db.session.rollback()

    # 2. Create Rider account
    existing = User.query.filter_by(email='rider@lemaison.com').first()
    if not existing:
        rider = User(
            first_name='Le Maison',
            last_name='Rider',
            username='rider1',
            email='rider@lemaison.com',
            role='RIDER',
            status='ACTIVE',
            is_verified=True,
        )
        rider.set_password('rider123')
        db.session.add(rider)
        db.session.commit()
        print(f"Rider account created: rider@lemaison.com / rider123")
    else:
        existing.role = 'RIDER'
        existing.status = 'ACTIVE'
        existing.is_verified = True
        db.session.commit()
        print(f"Rider account already exists, role updated to RIDER.")

    print("\nDone! Rider setup complete.")
