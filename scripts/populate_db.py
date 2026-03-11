from app import app
from models import db, User, MenuItem, Reservation, Order, OrderItem, Review
from datetime import datetime, date, timedelta
import random

def populate_database():
    with app.app_context():
        # WARNING: This will drop and recreate all tables in whatever database is specified in .env!
        print("Recreating database schema (Dropping old data)...")
        db.drop_all()
        db.create_all()

        print("Creating an Admin user...")
        # ─── ADMIN USER ───
        admin = User(
            first_name="Store",
            last_name="Owner",
            username="admin",
            email="admin@gmail.com",
            birthday=date(2000, 1, 1),
            status="ACTIVE",
            role="ADMIN",
            is_verified=True
        )
        admin.set_password("Admin123!")
        db.session.add(admin)

        print("Creating Sample Regular Customers...")
        # ─── USERS ───
        user_data = [
            ("Juan", "Dela Cruz", "juan99", "juan99@gmail.com", "ACTIVE"),
            ("Maria", "Clara", "maria_c", "mariaclara@gmail.com", "PENDING"),
            ("Pedro", "Penduko", "pedro_p", "pedropenduko@gmail.com", "ACTIVE")
        ]
        
        users = []
        for first, last, uname, eml, status in user_data:
            u = User(
                first_name=first, last_name=last, username=uname,
                email=eml, birthday=date(1995, 5, 10), status=status, role="USER", is_verified=True
            )
            u.set_password("User123!")
            db.session.add(u)
            users.append(u)
        db.session.commit()

        print("Adding Sample Menu Items...")
        # ─── MENU ITEMS ───
        menu_items = [
            MenuItem(name="Le Maison Iced Coffee", description="Our signature iced local beans with smooth cream.", price=180.00, category="Iced Coffee", image_url="https://images.unsplash.com/photo-1517701550927-30cfcb64db10", is_available=True),
            MenuItem(name="Truffle Mushroom Pasta", description="Creamy pasta with authentic truffle oil and parmesan.", price=350.50, category="Pasta", image_url="https://images.unsplash.com/photo-1473093295043-cdd812d0e601", is_available=True),
            MenuItem(name="Classic Cheeseburger", description="Angus beef patty with melted cheese and fresh greens.", price=280.00, category="Mains", image_url="https://images.unsplash.com/photo-1568901346375-23c9450c58cd", is_available=True),
            MenuItem(name="Matcha Latte", description="Premium authentic matcha powder steamed to perfection.", price=195.00, category="Hot Drinks", image_url="https://images.unsplash.com/photo-1536281140500-77814b0b5550", is_available=True),
            MenuItem(name="French Fries", description="Crispy salted fries.", price=120.00, category="Sides", image_url="https://images.unsplash.com/photo-1576107232684-1279f3908592", is_available=False),
        ]
        db.session.add_all(menu_items)
        db.session.commit()

        print("Adding Sample Reservations...")
        # ─── RESERVATIONS ───
        res_data = [
            (users[0].id, date.today() + timedelta(days=2), datetime.strptime("18:30", "%H:%M").time(), 4, "Anniversary", "REGULAR", "CONFIRMED"),
            (users[0].id, date.today() + timedelta(days=5), datetime.strptime("12:00", "%H:%M").time(), 2, None, "REGULAR", "PENDING"),
            (users[2].id, date.today() - timedelta(days=1), datetime.strptime("14:00", "%H:%M").time(), 10, "Birthday", "EXCLUSIVE", "COMPLETED"),
        ]
        for uid, d, t, c, o, bt, s in res_data:
            r = Reservation(user_id=uid, date=d, time=t, guest_count=c, occasion=o, booking_type=bt, status=s)
            db.session.add(r)
        db.session.commit()

        print("Adding Sample Orders...")
        # ─── ORDERS ───
        o1 = Order(user_id=users[0].id, total_amount=530.50, status="COMPLETED", notes="No ketchup")
        o2 = Order(user_id=users[2].id, total_amount=195.00, status="PENDING", notes="Extra hot")
        
        db.session.add_all([o1, o2])
        db.session.commit()

        # Add items to Orders
        db.session.add_all([
            OrderItem(order_id=o1.id, menu_item_id=menu_items[0].id, quantity=1, price_at_time=180.00),
            OrderItem(order_id=o1.id, menu_item_id=menu_items[1].id, quantity=1, price_at_time=350.50),
            OrderItem(order_id=o2.id, menu_item_id=menu_items[3].id, quantity=1, price_at_time=195.00)
        ])
        db.session.commit()

        print("Adding Sample Reviews...")
        # ─── REVIEWS ───
        rev1 = Review(user_id=users[0].id, rating=5, comment="Amazing coffee and pasta! Will definitely come back.", status="APPROVED")
        rev2 = Review(user_id=users[2].id, rating=4, comment="Great place but wait time was a bit long.", status="PENDING")
        db.session.add_all([rev1, rev2])
        db.session.commit()

        print("==================================================")
        print("DATABASE SUCCESSFULLY POPULATED WITH SAMPLE DATA!")
        print("Admin Credentials:")
        print("Email: admin@gmail.com")
        print("Password: Admin123!")
        print("==================================================")

if __name__ == '__main__':
    populate_database()
