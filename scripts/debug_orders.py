from app import app
from models import Order, User
with app.app_context():
    print("--- LIVE ORDERS ---")
    orders = Order.query.all()
    for o in orders:
        print(f"ID: {o.id} | Dining: {o.dining_option} | Status: {o.status} | Rider: {o.rider_id} | DelivStatus: {o.delivery_status}")
    
    print("\n--- RIDER USERS ---")
    riders = User.query.filter_by(role='RIDER').all()
    for r in riders:
        print(f"ID: {r.id} | Name: {r.first_name} {r.last_name} | Email: {r.email}")
