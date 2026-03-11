from app import app
from models import db, User

if __name__ == '__main__':
    with app.app_context():
        # Kitchen Staff Account
        kitchen = User.query.filter_by(username='kitchen1').first()
        if not kitchen:
            kitchen = User(
                first_name='Staff',
                last_name='Kitchen',
                username='kitchen1',
                email='kitchen@lemaison.com',
                status='ACTIVE',
                role='KITCHEN',
                is_verified=True
            )
            kitchen.set_password('password123')
            db.session.add(kitchen)
            print("Created Kitchen Staff Account:")
            print("  Email: kitchen@lemaison.com")
            print("  Password: password123")
        else:
            print("Kitchen Staff Account already exists.")

        try:
            db.session.commit()
            print("\nSuccessfully saved to database!")
        except Exception as e:
            db.session.rollback()
            print(f"Error: {e}")
