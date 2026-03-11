from app import app
from models import Order, db
with app.app_context():
    order = Order(
        customer_name='Test Customer',
        total_amount=150.0,
        status='PREPARING',
        dining_option='DELIVERY',
        payment_method='COUNTER',
        payment_status='UNPAID',
        delivery_address='123 Test St, Laguna',
        delivery_status='WAITING'
    )
    db.session.add(order)
    db.session.commit()
    print(f'New Test Order Created: ID {order.id}')
