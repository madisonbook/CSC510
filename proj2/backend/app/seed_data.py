import asyncio
from datetime import datetime, timedelta
from .database import get_database
from .utils import hash_password


async def seed():
    db = get_database()
    users_count = await db.users.count_documents({})
    meals_count = await db.meals.count_documents({})
    if users_count == 0 and meals_count == 0:
        now = datetime.utcnow()

        users = [
            {
                "full_name": "Alice Johnson",
                "email": "alice@example.com",
                "password": hash_password("password123"),
                "verified": True,
                "role": "user",
                "status": "active",
                "location": {
                    "address": "123 Main St",
                    "city": "Springfield",
                    "state": "IL",
                    "zip_code": "62704",
                    "latitude": None,
                    "longitude": None,
                },
                "created_at": now,
                "updated_at": now,
            },
            {
                "full_name": "Bob Smith",
                "email": "bob@example.com",
                "password": hash_password("password123"),
                "verified": True,
                "role": "user",
                "status": "active",
                "location": {
                    "address": "456 Oak Ave",
                    "city": "Rivertown",
                    "state": "CA",
                    "zip_code": "90210",
                    "latitude": None,
                    "longitude": None,
                },
                "created_at": now,
                "updated_at": now,
            },
            {
                "full_name": "Admin User",
                "email": "admin@example.com",
                "password": hash_password("adminpass"),
                "verified": True,
                "role": "admin",
                "status": "active",
                "location": {
                    "address": "1 Admin Plaza",
                    "city": "Metropolis",
                    "state": "NY",
                    "zip_code": "10001",
                    "latitude": None,
                    "longitude": None,
                },
                "created_at": now,
                "updated_at": now,
            },
        ]

        result = await db.users.insert_many(users)

        email_to_id = {}
        for user_doc, inserted_id in zip(users, result.inserted_ids):
            email_to_id[user_doc["email"]] = inserted_id

        expires_short = now + timedelta(days=1)
        expires_long = now + timedelta(days=2)

        meals = [
            {
                "title": "Spaghetti Bolognese",
                "description": "Classic Italian pasta with meat sauce",
                "sale_price": 9.99,
                "cuisine_type": "Italian",
                "meal_type": "Dinner",
                "seller_id": email_to_id.get("alice@example.com"),
                "status": "available",
                "available_for_sale": True,
                "available_for_swap": False,
                "portion_size": "2 servings",
                "allergen_info": {"contains": [], "may_contain": []},
                "allergens": [],
                "photos": ["https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=800"],
                "pickup_instructions": "Pickup at front porch",
                "preparation_date": now,
                "expires_date": expires_short,
                "created_at": now,
                "updated_at": now,
            },
            {
                "title": "Vegan Buddha Bowl",
                "description": "Healthy mix of grains, veggies, and tofu",
                "sale_price": 11.5,
                "cuisine_type": "Vegan",
                "meal_type": "Lunch",
                "seller_id": email_to_id.get("bob@example.com"),
                "status": "available",
                "available_for_sale": True,
                "available_for_swap": False,
                "portion_size": "1 serving",
                "allergen_info": {"contains": [], "may_contain": []},
                "allergens": [],
                "photos": ["https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=800"],
                "pickup_instructions": "Pickup at side gate",
                "preparation_date": now,
                "expires_date": expires_long,
                "created_at": now,
                "updated_at": now,
            },
            {
                "title": "Chicken Curry",
                "description": "Spicy and savory curry",
                "sale_price": 10.75,
                "cuisine_type": "Indian",
                "meal_type": "Dinner",
                "seller_id": email_to_id.get("alice@example.com"),
                "status": "available",
                "available_for_sale": True,
                "available_for_swap": False,
                "portion_size": "3 servings",
                "allergen_info": {"contains": ["dairy"], "may_contain": []},
                "allergens": ["dairy"],
                "photos": ["https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=800"],
                "pickup_instructions": "Pickup at back door",
                "preparation_date": now,
                "expires_date": expires_long,
                "created_at": now,
                "updated_at": now,
            },
            {
                "title": "Tacos al Pastor",
                "description": "Marinated pork and pineapple",
                "sale_price": 8.25,
                "cuisine_type": "Mexican",
                "meal_type": "Dinner",
                "seller_id": email_to_id.get("bob@example.com"),
                "status": "available",
                "available_for_sale": True,
                "available_for_swap": False,
                "portion_size": "2 servings",
                "allergen_info": {"contains": [], "may_contain": []},
                "allergens": [],
                "photos": ["https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=800"],
                "pickup_instructions": "Pickup at mailbox",
                "preparation_date": now,
                "expires_date": expires_short,
                "created_at": now,
                "updated_at": now,
            },
        ]

        meals_result = await db.meals.insert_many(meals)

        print(f"✅ Seeded {len(result.inserted_ids)} users and {len(meals_result.inserted_ids)} meals")