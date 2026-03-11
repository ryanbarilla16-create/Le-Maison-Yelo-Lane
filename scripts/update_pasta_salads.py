from app import app
from models import db, MenuItem

items = [
    {"name": "Caesar Salad", "price": 385.00, "description": "Lettuce, Tomato, Croutons, Cucumber, Onion, Bacon, Caesar Dressing", "image_url": "https://i.postimg.cc/26xF4D5c/1.webp"},
    {"name": "Lasagna", "price": 365.00, "description": "Lasagna, Ground Beef, Cream, Tomato Sauce, Mozzarella, Garlic Bread", "image_url": "https://i.postimg.cc/g0FvQJX8/2.webp"},
    {"name": "Truffle Bacon", "price": 325.00, "description": "Fettucine, Cream, Truffle Paste, Mushroom, Parmesan, Garlic Bread", "image_url": "https://i.postimg.cc/26Th17cR/3.webp"},
    {"name": "Carbonara", "price": 325.00, "description": "Fettucine, Cream, Mushroom, Parmesan, Garlic Bread (Toppings: Tuna 229 | Shrimp 289 | Bacon, Chicken, 229)", "image_url": "https://i.postimg.cc/158wz6px/4.webp"},
    {"name": "Gourmet Tuyo Spaghetti", "price": 295.00, "description": "Spaghetti, Olive Oil, Garlic, Gourmet Tuyo", "image_url": "https://i.postimg.cc/G23snsc7/5.webp"},
    {"name": "Creamy Tomato Penne", "price": 229.00, "description": "Penne, Tomato, Cream, Mozzarella, Parmesan, Garlic Bread", "image_url": "https://i.postimg.cc/QxKKDDrk/6.webp"},
    {"name": "Bolognese", "price": 365.00, "description": "Spaghetti, Ground Beef, Tomato, Parmesan, Garlic Bread", "image_url": "https://i.postimg.cc/dV87793S/7.webp"},
    {"name": "Puttanesca", "price": 295.00, "description": "Spaghetti, Olives, Capers, Tomato, Parmesan, Garlic Bread", "image_url": "https://i.postimg.cc/LXshbKTc/8.webp"},
    {"name": "Filipino Spaghetti", "price": 295.00, "description": "Spaghetti, Ground Beef, Hotdog, Tomato, Parmesan, Garlic Bread", "image_url": "https://i.postimg.cc/d3b137Yw/9.webp"},
    {"name": "Italian Carbonara", "price": 329.00, "description": "Fettucine, Eggs, Guanciale, Parmigiano Reggiano, Garlic Bread", "image_url": "https://i.postimg.cc/28WyJxQS/10.webp"},
    {"name": "Pesto", "price": 325.00, "description": "Spaghetti, Parmesan, Pesto Sauce Served with Garlic Bread (Toppings: Tuna 229 | Shrimp 269 | Bacon, Chicken| 229)", "image_url": "https://i.postimg.cc/BbH8x5Nt/11.webp"},
    {"name": "Wagyu Salad", "price": 525.00, "description": "Lettuce, Croutons, Tomato, Cucumber, Onion, Bacon, Sesame Dressing, Grilled Wagyu", "image_url": "https://i.postimg.cc/yx4xYgB1/12.webp"},
    {"name": "Chicken Salad", "price": 495.00, "description": "Lettuce, Croutons, Tomato, Cucumber, Onion, Bacon, Caesar Dressing, Roasted Chicken Fillet", "image_url": "https://i.postimg.cc/yx4xYgB1/12.webp"},
]

def update_items():
    with app.app_context():
        category = "Pasta & Salads"
        for item_data in items:
            existing_item = MenuItem.query.filter_by(name=item_data['name']).first()
            if existing_item:
                existing_item.price = item_data['price']
                existing_item.description = item_data['description']
                existing_item.image_url = item_data['image_url']
                existing_item.category = category
                print(f"Updated: {item_data['name']}")
            else:
                new_item = MenuItem(
                    name=item_data['name'],
                    description=item_data['description'],
                    price=item_data['price'],
                    category=category,
                    image_url=item_data['image_url'],
                    is_available=True
                )
                db.session.add(new_item)
                print(f"Added: {item_data['name']}")
        
        db.session.commit()
        print("All items processed successfully.")

if __name__ == '__main__':
    update_items()
