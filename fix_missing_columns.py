"""
Migration: Add all missing columns to match the current models.py
Run once to update the existing database schema.
"""
from app import app, db
import sqlalchemy as sa

def add_column_if_missing(conn, inspector, table_name, column_name, column_def):
    columns = [col['name'] for col in inspector.get_columns(table_name)]
    if column_name not in columns:
        try:
            conn.execute(sa.text(f'ALTER TABLE "{table_name}" ADD COLUMN {column_name} {column_def}'))
            print(f"  + Added '{column_name}' to '{table_name}'")
            return True
        except Exception as e:
            print(f"  ! Error adding '{column_name}' to '{table_name}': {e}")
            return False
    else:
        print(f"  - '{column_name}' already exists in '{table_name}'")
        return False

with app.app_context():
    inspector = sa.inspect(db.engine)
    with db.engine.connect() as conn:
        print("=== Fixing missing columns ===\n")

        # Reservation table
        print("[reservation]")
        add_column_if_missing(conn, inspector, 'reservation', 'cancellation_reason', 'TEXT')
        add_column_if_missing(conn, inspector, 'reservation', 'duration', 'INTEGER DEFAULT 2')

        # Order table
        print("\n[order]")
        add_column_if_missing(conn, inspector, 'order', 'reservation_id', 'INTEGER REFERENCES reservation(id)')
        add_column_if_missing(conn, inspector, 'order', 'prep_start_at', 'TIMESTAMP')
        add_column_if_missing(conn, inspector, 'order', 'prep_end_at', 'TIMESTAMP')
        add_column_if_missing(conn, inspector, 'order', 'prep_duration', 'INTEGER')
        add_column_if_missing(conn, inspector, 'order', 'estimated_cost', 'NUMERIC(10,2) DEFAULT 0')
        add_column_if_missing(conn, inspector, 'order', 'processed_by_id', 'INTEGER REFERENCES "user"(id)')
        add_column_if_missing(conn, inspector, 'order', 'xendit_invoice_id', 'VARCHAR(255)')
        add_column_if_missing(conn, inspector, 'order', 'xendit_invoice_url', 'VARCHAR(255)')
        add_column_if_missing(conn, inspector, 'order', 'proof_of_delivery_url', 'VARCHAR(255)')

        # User table
        print("\n[user]")
        add_column_if_missing(conn, inspector, 'user', 'wallet_balance', 'NUMERIC(10,2) DEFAULT 0')
        add_column_if_missing(conn, inspector, 'user', 'profile_picture_url', 'VARCHAR(500)')

        conn.commit()
        print("\n=== Done! All columns verified. ===")
