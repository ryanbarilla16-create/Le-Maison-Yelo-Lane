
print(f"""
DROP TABLE IF EXISTS "review" CASCADE;
DROP TABLE IF EXISTS "order_item" CASCADE;
DROP TABLE IF EXISTS "order" CASCADE;
DROP TABLE IF EXISTS "reservation" CASCADE;
DROP TABLE IF EXISTS "menu_item" CASCADE;
DROP TABLE IF EXISTS "user" CASCADE;

CREATE TABLE "user" (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    middle_name VARCHAR(50),
    last_name VARCHAR(50) NOT NULL,
    username VARCHAR(20) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    birthday DATE NOT NULL,
    password_hash VARCHAR(256) NOT NULL,
    status VARCHAR(20) DEFAULT 'PENDING',
    role VARCHAR(20) DEFAULT 'USER',
    is_verified BOOLEAN DEFAULT FALSE,
    otp_code VARCHAR(6),
    otp_created_at TIMESTAMP
);

CREATE TABLE "menu_item" (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    price NUMERIC(10, 2) NOT NULL,
    category VARCHAR(50) NOT NULL,
    image_url VARCHAR(255),
    is_available BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE "reservation" (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES "user"(id) NOT NULL,
    date DATE NOT NULL,
    time TIME NOT NULL,
    guest_count INTEGER NOT NULL,
    occasion VARCHAR(50),
    booking_type VARCHAR(20) NOT NULL,
    status VARCHAR(20) DEFAULT 'PENDING',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE "order" (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES "user"(id) NOT NULL,
    total_amount NUMERIC(10, 2) NOT NULL,
    status VARCHAR(20) DEFAULT 'PENDING',
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE "order_item" (
    id SERIAL PRIMARY KEY,
    order_id INTEGER REFERENCES "order"(id) NOT NULL,
    menu_item_id INTEGER REFERENCES "menu_item"(id) NOT NULL,
    quantity INTEGER NOT NULL,
    price_at_time NUMERIC(10, 2) NOT NULL
);

CREATE TABLE "review" (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES "user"(id) NOT NULL,
    rating INTEGER NOT NULL,
    comment TEXT,
    status VARCHAR(20) DEFAULT 'PENDING',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- MOCK DATA

INSERT INTO "user" (id, first_name, last_name, username, email, birthday, password_hash, status, role, is_verified) VALUES 
(1, 'Store', 'Owner', 'admin', 'admin@gmail.com', '2000-01-01', 'pbkdf2:sha256:260000$ia0oz8xsRaVzwvRh$14beee9b6ef47ad25c3c48eaad4e9a4999a897c9a8160963d3c45421c5b29ca0', 'ACTIVE', 'ADMIN', true),
(2, 'Juan', 'Dela Cruz', 'juan99', 'juan99@gmail.com', '1995-05-10', 'pbkdf2:sha256:260000$386UUvu1heH1PAI7$a92fb070506c00e403706f299b8f85134fdfba9f54d12c26e10969af3ef3f77e', 'ACTIVE', 'USER', true),
(3, 'Pedro', 'Penduko', 'pedro_p', 'pedropenduko@gmail.com', '1998-08-20', 'pbkdf2:sha256:260000$386UUvu1heH1PAI7$a92fb070506c00e403706f299b8f85134fdfba9f54d12c26e10969af3ef3f77e', 'PENDING', 'USER', true);

SELECT setval('user_id_seq', 3);

INSERT INTO "menu_item" (id, name, description, price, category, image_url, is_available) VALUES 
(1, 'Le Maison Iced Coffee', 'Our signature iced local beans with smooth cream.', 180.00, 'Iced Coffee', 'https://images.unsplash.com/photo-1517701550927-30cfcb64db10', true),
(2, 'Truffle Mushroom Pasta', 'Creamy pasta with authentic truffle oil and parmesan.', 350.50, 'Pasta', 'https://images.unsplash.com/photo-1473093295043-cdd812d0e601', true),
(3, 'Classic Cheeseburger', 'Angus beef patty with melted cheese and fresh greens.', 280.00, 'Mains', 'https://images.unsplash.com/photo-1568901346375-23c9450c58cd', true),
(4, 'Matcha Latte', 'Premium authentic matcha powder steamed to perfection.', 195.00, 'Hot Drinks', 'https://images.unsplash.com/photo-1536281140500-77814b0b5550', true);

SELECT setval('menu_item_id_seq', 4);

INSERT INTO "reservation" (id, user_id, date, time, guest_count, occasion, booking_type, status) VALUES 
(1, 2, '2026-03-05', '18:30:00', 4, 'Anniversary', 'REGULAR', 'CONFIRMED'),
(2, 2, '2026-03-10', '12:00:00', 2, NULL, 'REGULAR', 'PENDING');

SELECT setval('reservation_id_seq', 2);

INSERT INTO "order" (id, user_id, total_amount, status, notes) VALUES 
(1, 2, 530.50, 'COMPLETED', 'No ketchup');

SELECT setval('order_id_seq', 1);

INSERT INTO "order_item" (id, order_id, menu_item_id, quantity, price_at_time) VALUES 
(1, 1, 1, 1, 180.00),
(2, 1, 2, 1, 350.50);

SELECT setval('order_item_id_seq', 2);

INSERT INTO "review" (id, user_id, rating, comment, status) VALUES 
(1, 2, 5, 'Amazing coffee and pasta! Will definitely come back.', 'APPROVED'),
(2, 3, 4, 'Great place but wait time was a bit long.', 'PENDING');

SELECT setval('review_id_seq', 2);
""")
    