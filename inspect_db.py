from app import app, db
import sqlalchemy as sa

with app.app_context():
    inspector = sa.inspect(db.engine)
    for table_name in inspector.get_table_names():
        print(f"Table: {table_name}")
        for column in inspector.get_columns(table_name):
            print(f"  - {column['name']} ({column['type']})")
        print("-" * 20)
