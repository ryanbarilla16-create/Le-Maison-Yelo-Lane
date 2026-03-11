from app import app
from models import db, MenuItem

rice_plates = [
    {"name": "Baby Back Ribs", "price": 425.00, "description": "Smoked Baby Back Ribs, Bbq Sauce, Rice, Veggies", "image_url": "https://i.postimg.cc/hPm8rTh8/1.webp", "category": "Rice Plates"},
    {"name": "Lechon Kawali", "price": 365.00, "description": "Fried Pork Belly, Rice, Vinegar Dipping Sauce, Side Salad", "image_url": "https://i.postimg.cc/s1Ch8H14/2.webp", "category": "Rice Plates"},
    {"name": "Grilled Salmon Steak", "price": 425.00, "description": "Grilled Salmon Steak, Mango Salsa, Veggies, Rice, Lemon Wedge", "image_url": "https://i.postimg.cc/VNfqKGHx/3.webp", "category": "Rice Plates"},
    {"name": "Grilled Herb Chicken", "price": 365.00, "description": "Grilled Chicken Leg Fillet, Italian Herbs & Spices, Garlic Yogurt Sauce, Rice, Side Salad or Veggies", "image_url": "https://i.postimg.cc/QCT1FRH3/4.webp", "category": "Rice Plates"},
    {"name": "Beef Schintzel", "price": 449.00, "description": "Fried T-Bone Steak Coated with Breadcrumbs and Spices, Served With Gravy, Side Salad and Rice", "image_url": "https://i.postimg.cc/XNR9R7zY/5.webp", "category": "Rice Plates"},
    {"name": "Chicken Wings w/ Rice", "price": 329.00, "description": "Fried Chicken Wings, Dipping Sauce, Rice (Available Flavors: Buffalo, Hickory BBQ or Sweet Chili)", "image_url": "https://i.postimg.cc/CxYkKr0W/6.webp", "category": "Rice Plates"},
    {"name": "Beef Salpicao", "price": 495.00, "description": "Ribeye Steak Stir-Fried in Garlic, Soy Sauce, Worcetershire Sauce, Served with Rice and Side Salad", "image_url": "https://i.postimg.cc/P54Zvbr6/7.webp", "category": "Rice Plates"},
    {"name": "Brown Butter Fish Fillet", "price": 345.00, "description": "Baked Fish Fillet in Calamansi Butter Sauce, Rice, Side Salad or Veggies", "image_url": "https://i.postimg.cc/Y94mPJNX/8.webp", "category": "Rice Plates"},
    {"name": "Chicken Drumsticks", "price": 365.00, "description": "Deep Fried 3 Piece Chicken Drumsticks, Rice, Side Salad or Veggies", "image_url": "https://i.postimg.cc/85rj4LD3/9.webp", "category": "Rice Plates"},
    {"name": "Black Pepper Pork Steak", "price": 385.00, "description": "Grilled Pork Chops, Black Pepper Sauce, Rice, Veggies", "image_url": "https://i.postimg.cc/brxdc8ZT/10.webp", "category": "Rice Plates"}
]

starters_sandwiches = [
    {"name": "Flavored Fries", "price": 195.00, "description": "Deep Fried Potatoes (Available Flavors: Sour Cream, Cheese, Barbecue)", "image_url": "https://i.postimg.cc/vTYwTdPW/1.webp", "category": "Starters & Sandwiches"},
    {"name": "Croque Monsieur", "price": 269.00, "description": "Ham & Cheese Sandwich Made with Gruyere, Parmesan, Ham and Bechamel Sauce (Variants: Croque Monsieur, Croque Madame)", "image_url": "https://i.postimg.cc/8CM2bC9F/2.webp", "category": "Starters & Sandwiches"},
    {"name": "Croissant Sandwich", "price": 349.00, "description": "Maple Ham, Lettuce, Cucumber, Tomato, Cheese, Housemade Croissant", "image_url": "https://i.postimg.cc/Hxmfvg16/3.webp", "category": "Starters & Sandwiches"},
    {"name": "Fish & Chips", "price": 345.00, "description": "Deep Fried Fish Fillet Coated with Special Beer Batter, Served with French Fries & Dipping Sauce", "image_url": "https://i.postimg.cc/rm97vP8t/4.webp", "category": "Starters & Sandwiches"},
    {"name": "French Fries", "price": 165.00, "description": "Deep Fried Potatoes with Ketchup & Mayo", "image_url": "https://i.postimg.cc/prG4d5h1/5.webp", "category": "Starters & Sandwiches"},
    {"name": "Chicken Wings", "price": 285.00, "description": "Deep Fried Chicken Wings Coated in Sauce of Choice (Available Flavors: Buffalo, Hickory Soy Garlic & Sweet Chili)", "image_url": "https://i.postimg.cc/4yLq3HHY/6.webp", "category": "Starters & Sandwiches"},
    {"name": "Mojos", "price": 225.00, "description": "Deep Fried Seasoned Potato Wedges with Ketchup and Mayo", "image_url": "https://i.postimg.cc/DyNRksKb/7.webp", "category": "Starters & Sandwiches"},
    {"name": "Nachos", "price": 365.00, "description": "Tortilla Chips, Mexican Beef, Fresh Salsa, Tomato Salsa, Cheese Sauce", "image_url": "https://i.postimg.cc/2SBMz6kN/8.webp", "category": "Starters & Sandwiches"},
    {"name": "Mushroom Soup", "price": 295.00, "description": "Bread Bowl, Truffle Paste, Cream, Shiitake Mushroom", "image_url": "https://i.postimg.cc/mrfqhskQ/9.webp", "category": "Starters & Sandwiches"},
    {"name": "Clubhouse Sandwich", "price": 289.00, "description": "Loaf Bread, Ham, Cheese, Cucumber, Tomato Lettuce, Mayonnaise, French Fries", "image_url": "https://i.postimg.cc/0Q9Bd0pq/10.webp", "category": "Starters & Sandwiches"},
    {"name": "Pork Sisig", "price": 395.00, "description": "Pork Belly, Pig Ears, Egg, Seasoned with Calamansi and Chilies Served on Sizzling Plate", "image_url": "https://i.postimg.cc/hv5ZnFNd/11.webp", "category": "Starters & Sandwiches"},
    {"name": "Le Maison Burger", "price": 375.00, "description": "Brioche Bun, Wagyu Patty, Mayo, Ketchup, Mustard, Cheese, Cucumber, Lettuce, Tomato", "image_url": "https://i.postimg.cc/8PxXnSRV/12.webp", "category": "Starters & Sandwiches"}
]

steaks = [
    {"name": "Grilled Burger Steak", "price": 395.00, "description": "Grilled Beef Patties, Gravy, Rice, Salad or Veggies", "image_url": "https://i.postimg.cc/FzdgjYnF/1.webp", "category": "Steaks"},
    {"name": "Grilled Porterhouse Steak", "price": 445.00, "description": "Grilled Porterhouse Steak, Rice, Gravy, Side Salad", "image_url": "https://i.postimg.cc/5yh5pfZp/2.webp", "category": "Steaks"},
    {"name": "Angus Ribeye Steak", "price": 785.00, "description": "150g Angus Ribeye Steak, Gravy, Rice, Veggies", "image_url": "https://i.postimg.cc/h46NNTny/3.webp", "category": "Steaks"},
    {"name": "Brazilian Ribeye Steak", "price": 385.00, "description": "Grilled Brazilian Ribeye Steak, Gravy, Salad or Veggies", "image_url": "https://i.postimg.cc/wjdZjz7H/4.webp", "category": "Steaks"},
    {"name": "Grilled T-Bone Steak", "price": 425.00, "description": "Grilled T-Bone Steak, Gravy, Rice, Side Salad or Veggies", "image_url": "https://i.postimg.cc/nhY5sWDd/5.webp", "category": "Steaks"},
    {"name": "Angus Beef Pepper Rice", "price": 325.00, "description": "Thinly Sliced USDA Beef Shortplate, Rice, Buttered Corn, Yakiniku Sauce", "image_url": "https://i.postimg.cc/1zvjBNMm/6.webp", "category": "Steaks"},
    {"name": "Steaks & Fries", "price": 895.00, "description": "Angus Ribeye Steak, Fries, Side Salad & Gravy", "image_url": "https://i.postimg.cc/k4DhpXhx/7.webp", "category": "Steaks"},
    {"name": "Saikoro Wagyu Cubes", "price": 345.00, "description": "8 Piece Saikoro Wagyu Cubes, Gravy, Rice, Salad or Veggies", "image_url": "https://i.postimg.cc/vBjSFFJF/8.webp", "category": "Steaks"},
    {"name": "USDA Ribeye Steak", "price": 1795.00, "description": "350g-450g USDA Choice Ribeye Steak, Gravy Rice, Veggies", "image_url": "https://i.postimg.cc/DfJMQ0Gh/9.webp", "category": "Steaks"}
]

sweet_breakfast = [
    {"name": "Classic Maple Waffles", "price": 199.00, "description": "Buttermilk Waffles, Butter, Maple Syrup", "image_url": "https://i.postimg.cc/RFjGp1tq/1.webp", "category": "Sweet Breakfast"},
    {"name": "Banana Nutella Waffles", "price": 249.00, "description": "Buttermilk Waffles, Nutella, Banana, Maple Syrup, Chocolate Chips, Almonds", "image_url": "https://i.postimg.cc/hvTskJ8k/2.webp", "category": "Sweet Breakfast"},
    {"name": "Nutella Banana Crepe", "price": 325.00, "description": "Crepe, Banana, Nutella, Chocolate Chips", "image_url": "https://i.postimg.cc/pVFsh7Nc/3.webp", "category": "Sweet Breakfast"},
    {"name": "Classic Maple Pancakes", "price": 265.00, "description": "Buttermilk Pancakes, Whipped Butter, Maple Syrup", "image_url": "https://i.postimg.cc/150MMq5L/4.webp", "category": "Sweet Breakfast"},
    {"name": "Banana Nutella Pancakes", "price": 325.00, "description": "Buttermilk Pancakes, Nutella Spread, Banana, Chocolate Chips, Almonds", "image_url": "https://i.postimg.cc/htSsYtXs/5.webp", "category": "Sweet Breakfast"}
]

thin_crust_pizza = [
    {"name": "Shawarma", "price": 449.00, "description": "Hand Tossed Pizza Dough, Pizza Sauce, Ground Beef, Tomato, Onion, Lettuce, Garlic Sauce, Cheese Sauce, Mozzarella", "image_url": "https://i.postimg.cc/5NpL6qt7/1.webp", "category": "Thin Crust Pizza"},
    {"name": "Chicken Pesto", "price": 429.00, "description": "Hand Tossed Pizza Dough, Pesto Sauce, Tomato, Parmesan Grilled Chicken, Mozzarella", "image_url": "https://i.postimg.cc/mr1HXvyq/2.webp", "category": "Thin Crust Pizza"},
    {"name": "Four Cheese", "price": 485.00, "description": "Hand Tossed Pizza Dough, Pizza Sauce, Ground Beef, Italian Pizza Sauce, Gouda, Mozzarella, Cheddar, Parmesan", "image_url": "https://i.postimg.cc/50wF18GH/3.webp", "category": "Thin Crust Pizza"},
    {"name": "Pepperoni", "price": 515.00, "description": "Hand Tossed Pizza Dough, Pizza Sauce, Smoked Pepperoni, Mozzarella", "image_url": "https://i.postimg.cc/MH5Mfqzq/4.webp", "category": "Thin Crust Pizza"},
    {"name": "Garlic Shrimp ", "price": 449.00, "description": "Hand Tossed Pizza Dough, White Sauce, Shrimp Garlic, Mozzarella, Parmesan", "image_url": "https://i.postimg.cc/VL70Yf7t/5.webp", "category": "Thin Crust Pizza"},
    {"name": "Loaded", "price": 565.00, "description": "Hand Tossed Pizza Dough, Pizza Sauce, Ground Beef, Italian Herbs and Spices, Onion, Bell Pepper,. Mushroom, Olives", "image_url": "https://i.postimg.cc/g2QwZMb6/6.webp", "category": "Thin Crust Pizza"},
    {"name": "Hawaiian", "price": 525.00, "description": "Hand Tossed Pizza Dough, Pizza Sauce, Farmer's Ham, Pineapple, Mozzarella", "image_url": "https://i.postimg.cc/vBdcPcBm/7.webp", "category": "Thin Crust Pizza"},
    {"name": "Meatlovers", "price": 565.00, "description": "Hand Tossed Pizza Dough, Pizza Sauce, Ground Beef, Honey Cured Bacon, Farmer's Ham, Mozzarella", "image_url": "https://i.postimg.cc/kGTGXsyC/8.webp", "category": "Thin Crust Pizza"},
    {"name": "Miele Al Tartufo", "price": 585.00, "description": "White Sauce, Provolone, Gouda, Mozzarella, Parmesan, Truffle Paste, Honey", "image_url": "https://i.postimg.cc/Yqy05X9g/9.webp", "category": "Thin Crust Pizza"},
    {"name": "Prosciutto Cotto", "price": 449.00, "description": "Tomato Sauce, Mozzarella, Prosciutto, Arugula", "image_url": "https://i.postimg.cc/pTxLf4GP/10.webp", "category": "Thin Crust Pizza"},
    {"name": "Quattro Formaggi", "price": 565.00, "description": "White Sauce, Provolone, Gouda, Mozzarella, Parmesan, Truffle Paste", "image_url": "https://i.postimg.cc/zv2D1BJV/11.webp", "category": "Thin Crust Pizza"}
]

all_items = rice_plates + starters_sandwiches + steaks + sweet_breakfast + thin_crust_pizza

def update_db():
    with app.app_context():
        for item_data in all_items:
            # Let's clean up name space
            name = item_data['name'].strip()
            existing_item = MenuItem.query.filter_by(name=name).first()
            if existing_item:
                existing_item.price = item_data['price']
                existing_item.description = item_data['description']
                existing_item.image_url = item_data['image_url']
                existing_item.category = item_data['category']
                print(f"Updated: {name}")
            else:
                new_item = MenuItem(
                    name=name,
                    description=item_data['description'],
                    price=item_data['price'],
                    category=item_data['category'],
                    image_url=item_data['image_url'],
                    is_available=True
                )
                db.session.add(new_item)
                print(f"Added: {name}")
        
        db.session.commit()
        print(f"Processed {len(all_items)} items successfully.")

if __name__ == '__main__':
    update_db()
