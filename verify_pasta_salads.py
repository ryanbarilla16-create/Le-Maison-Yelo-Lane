from app import app
from models import db, MenuItem

items_to_check = [
    "Caesar Salad", "Lasagna", "Truffle Bacon", "Carbonara", "Gourmet Tuyo Spaghetti",
    "Creamy Tomato Penne", "Bolognese", "Puttanesca", "Filipino Spaghetti",
    "Italian Carbonara", "Pesto", "Wagyu Salad", "Chicken Salad"
]

def check_items():
    with app.app_context():
        with open("pasta_check.txt", "w") as f:
            for name in items_to_check:
                item = MenuItem.query.filter_by(name=name).first()
                if item:
                    f.write(f"Name: {item.name}, Price: {item.price}, Category: {item.category}, Img: {item.image_url}\n")
                else:
                    f.write(f"MISSING: {name}\n")

if __name__ == '__main__':
    check_items()
