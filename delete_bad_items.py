from app import app
from models import db, MenuItem

def delete_bad_items():
    with app.app_context():
        bad_items = MenuItem.query.filter(MenuItem.name.like('%hatdoghatdog%')).all()
        for item in bad_items:
            db.session.delete(item)
            print(f"Deleted bad item: {item.id}")
        db.session.commit()
        print("Done.")

if __name__ == '__main__':
    delete_bad_items()
