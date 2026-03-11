import json
from app import app
from models import Order, User

with app.app_context():
    print("--- ALL ORDERS IN DB ---")
    all_orders = Order.query.all()
    for o in all_orders:
        print(f"ID: {o.id} | Dining: {o.dining_option} | Status: {o.status} | Rider: {o.rider_id} | DelivStatus: {o.delivery_status}")
    
    # Simulate the rider dashboard request for rider 13
    print("\n--- SIMULATING DASHBOARD FOR RIDER 13 ---")
    rider_id = 13
    
    available = Order.query.filter(
        Order.dining_option == 'DELIVERY',
        Order.status.in_(['PENDING', 'PREPARING', 'COMPLETED']),
        (Order.rider_id == None) | (Order.delivery_status == 'WAITING')
    ).all()
    
    my_active = Order.query.filter(
        Order.rider_id == rider_id,
        Order.delivery_status.in_(['PICKED_UP', 'ON_THE_WAY'])
    ).all()
    
    from utils import get_ph_time
    import datetime
    today_start = get_ph_time().replace(hour=0, minute=0, second=0, microsecond=0)
    my_completed = Order.query.filter(
        Order.rider_id == rider_id,
        Order.delivery_status == 'DELIVERED',
        Order.created_at >= today_start
    ).all()
    
    print(f"AVAILABLE COUNT: {len(available)}")
    for a in available: print(f"  - Available: ID {a.id}")
    
    print(f"ACTIVE COUNT: {len(my_active)}")
    for act in my_active: print(f"  - Active: ID {act.id}")
    
    print(f"COMPLETED COUNT: {len(my_completed)}")
    for c in my_completed: print(f"  - Completed: ID {c.id}")
