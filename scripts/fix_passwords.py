"""
One-time script to fix scrypt password hashes in the database.
Run this once, then delete this file.
"""
import sys
sys.path.insert(0, '.')

from app import app, db
from models import User
from werkzeug.security import generate_password_hash

with app.app_context():
    users = User.query.all()
    fixed = 0
    for user in users:
        if user.password_hash and user.password_hash.startswith('scrypt:'):
            # Replace broken scrypt hash with pbkdf2 hash for "Secret@123"
            user.password_hash = generate_password_hash('Secret@123', method='pbkdf2:sha256')
            fixed += 1
            print(f"  Fixed: {user.email}")
    
    if fixed > 0:
        db.session.commit()
        print(f"\n✅ Done! Fixed {fixed} user(s). Password is: Secret@123")
    else:
        print("✅ No broken hashes found. All good!")
