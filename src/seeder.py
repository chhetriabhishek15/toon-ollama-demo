import sqlite3
from faker import Faker
import random
import os

# Seeder: create users.db with sample data
fake = Faker('en_US')

user_records = []
foods = [
    "Pizza", "Sushi", "Tacos", "Pasta", "Burger",
    "Steak", "Salad", "Curry", "Pho", "Ramen",
]

print("✨ Generating 50 sample user records...")

for i in range(50):
    record = (
        fake.name(),
        random.randint(18, 65),
        random.choice(foods),
        fake.city()
    )
    user_records.append(record)

DB_NAME = 'users.db'
if os.path.exists(DB_NAME):
    os.remove(DB_NAME)

try:
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            age INTEGER,
            fav_food TEXT,
            city TEXT
        );
    """)

    cursor.executemany("""
        INSERT INTO users (name, age, fav_food, city)
        VALUES (?, ?, ?, ?);
    """, user_records)
    conn.commit()
    print(f"✅ Successfully inserted {cursor.rowcount} records.")

    print("\n📝 Sample (first 5 records):")
    cursor.execute("SELECT * FROM users LIMIT 5;")
    column_names = [description[0] for description in cursor.description]
    print("-" * 60)
    print(f"{column_names[0]:<3} | {column_names[1]:<20} | {column_names[2]:<3} | {column_names[3]:<12} | {column_names[4]:<15}")
    print("-" * 60)
    for row in cursor.fetchall():
        print(f"{row[0]:<3} | {row[1]:<20} | {row[2]:<3} | {row[3]:<12} | {row[4]:<15}")

except sqlite3.Error as e:
    print(f"An SQLite error occurred: {e}")

finally:
    if conn:
        conn.close()
        print("\n✅ Database connection closed.")
