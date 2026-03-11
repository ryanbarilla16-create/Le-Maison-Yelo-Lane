import sys
import os

from app import app
from models import db, User

if __name__ == '__main__':
    with app.app_context():
        # Cashier Account
        cashier = User.query.filter_by(username='cashier1').first()
        if not cashier:
            cashier = User(
                first_name='Staff',
                last_name='Cashier',
                username='cashier1',
                email='cashier@lemaison.com',
                status='ACTIVE',
                role='CASHIER',
                is_verified=True
            )
            cashier.set_password('password123')
            db.session.add(cashier)
            print("Created Cashier Account: cashier1 / password123")
        else:
            print("Cashier Account already exists.")

        # Inventory Staff Account
        inventory = User.query.filter_by(username='inventory1').first()
        if not inventory:
            inventory = User(
                first_name='Staff',
                last_name='Inventory',
                username='inventory1',
                email='inventory@lemaison.com',
                status='ACTIVE',
                role='INVENTORY_STAFF',
                is_verified=True
            )
            inventory.set_password('password123')
            db.session.add(inventory)
            print("Created Inventory Staff Account: inventory1 / password123")
        else:
            print("Inventory Staff Account already exists.")

        try:
            db.session.commit()
            print("Successfully saved accounts to the database.")
        except Exception as e:
            db.session.rollback()
            print(f"Error saving accounts: {e}")
