from app import app
from models import Order
with app.app_context():
    orders = Order.query.filter_by(dining_option='DELIVERY').all()
    print('DELIVERY ORDERS:')
    for o in orders:
        print(f'ID: {o.id}, Status: {o.status}, Rider: {o.rider_id}, DeliveryStatus: {o.delivery_status}')
