import asyncio
from datetime import datetime
from .database import get_database

async def seed():
    db = get_database()
    users_count = await db.users.count_documents({})
    meals_count = await db.meals.count_documents({})
    if users_count == 0 and meals_count == 0:
        now = datetime.utcnow()
        await db.users.insert_many([
            {"full_name":"Alice Johnson","email":"alice@example.com","password":"$2b$12$seedpwd","verified":True,"role":"user","status":"active","created_at":now,"updated_at":now},
            {"full_name":"Bob Smith","email":"bob@example.com","password":"$2b$12$seedpwd","verified":True,"role":"user","status":"active","created_at":now,"updated_at":now},
            {"full_name":"Admin User","email":"admin@example.com","password":"$2b$12$seedpwd","verified":True,"role":"admin","status":"active","created_at":now,"updated_at":now},
        ])
        await db.meals.insert_many([
            {"title":"Spaghetti Bolognese","description":"Classic Italian pasta with meat sauce","price":9.99,"cuisine_type":"Italian","seller_email":"alice@example.com","status":"published","created_at":now,"updated_at":now},
            {"title":"Vegan Buddha Bowl","description":"Healthy mix of grains, veggies, and tofu","price":11.5,"cuisine_type":"Vegan","seller_email":"bob@example.com","status":"published","created_at":now,"updated_at":now},
            {"title":"Chicken Curry","description":"Spicy and savory curry","price":10.75,"cuisine_type":"Indian","seller_email":"alice@example.com","status":"published","created_at":now,"updated_at":now},
            {"title":"Tacos al Pastor","description":"Marinated pork and pineapple","price":8.25,"cuisine_type":"Mexican","seller_email":"bob@example.com","status":"published","created_at":now,"updated_at":now},
        ])