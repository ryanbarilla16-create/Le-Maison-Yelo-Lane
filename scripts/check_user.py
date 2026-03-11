from app import app
from models import User
with app.app_context():
    u = User.query.filter_by(email='rider@lemaison.com').first()
    if u:
        print(f'ID: {u.id}, Role: {u.role}')
    else:
        print('User not found')
