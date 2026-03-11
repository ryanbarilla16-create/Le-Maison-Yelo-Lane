import os

routes_dir = r"c:\Users\Ryan Bien Barilla\OneDrive\Desktop\python web (capstone)\routes"
files = ["admin.py", "auth.py", "orders.py", "reservations.py", "views.py"]

for f in files:
    name = f[:-3]
    path = os.path.join(routes_dir, f)
    if os.path.exists(path):
        folder_path = os.path.join(routes_dir, name)
        os.makedirs(folder_path, exist_ok=True)
        new_path = os.path.join(folder_path, "__init__.py")
        
        with open(path, "r", encoding="utf-8") as file:
            content = file.read()
            
        # Update the import to go up one package (from . import main_bp -> from .. import main_bp)
        content = content.replace("from . import main_bp", "from .. import main_bp")
        
        with open(new_path, "w", encoding="utf-8") as file:
            file.write(content)
            
        os.remove(path)

print("Migration completed.")
