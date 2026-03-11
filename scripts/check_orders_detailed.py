from app import app
from models import Order
with app.app_context():
    orders = Order.query.all()
    print(f'TOTAL ORDERS: {len(orders)}')
    for o in orders:
        print(f'ID: {o.id}, Dining: {o.dining_option}, Status: {o.status}, Rider: {o.rider_id}, DelivStatus: {o.delivery_status}')
