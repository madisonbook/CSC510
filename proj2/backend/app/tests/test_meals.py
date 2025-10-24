import pytest
import pytest_asyncio
import asyncio
import os
from datetime import datetime, timedelta
from httpx import AsyncClient
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import FastAPI
from bson import ObjectId

from app.main import app
from app.database import get_database
from app.dependencies import get_current_user
from app.models import MealStatus, UserRole, AccountStatus

# Import test configuration from conftest
# These are set via environment variables in Docker
from .conftest import TEST_MONGO_URL, TEST_DB_NAME

# Debug print
print(f"\n[test_meals.py] Using TEST_MONGO_URL: {TEST_MONGO_URL}")
print(f"[test_meals.py] Using TEST_DB_NAME: {TEST_DB_NAME}\n")

# NOTE: mongo_client fixture is provided by conftest.py

# Remove this fixture - it's defined in conftest.py
# The mongo_client fixture from conftest.py will be used instead

@pytest_asyncio.fixture(scope="function")
async def db(mongo_client):
    """Get test database and clean it before each test."""
    # Use the mongo_client from conftest.py which has the correct URL
    database = mongo_client[TEST_DB_NAME]
    
    # Clean up collections before each test
    await database.meals.delete_many({})
    await database.users.delete_many({})
    await database.reviews.delete_many({})
    
    yield database
    
    # Clean up after test
    await database.meals.delete_many({})
    await database.users.delete_many({})
    await database.reviews.delete_many({})

@pytest_asyncio.fixture
async def test_user(db):
    """Create a test user."""
    user_data = {
        "_id": ObjectId(),
        "email": "testuser@example.com",
        "full_name": "Test User",
        "phone": "1234567890",
        "location": {
            "address": "123 Test St",
            "city": "Test City",
            "state": "TS",
            "zip_code": "12345"
        },
        "bio": "Test bio",
        "profile_picture": None,
        "dietary_preferences": {
            "dietary_restrictions": [],
            "allergens": [],
            "cuisine_preferences": []
        },
        "social_media": {},
        "role": UserRole.USER,
        "status": AccountStatus.ACTIVE,
        "stats": {
            "total_meals_sold": 0,
            "total_meals_swapped": 0,
            "total_meals_purchased": 0,
            "average_rating": 4.5,
            "total_reviews": 10,
            "badges": []
        },
        "verified": True,
        "created_at": datetime.utcnow()
    }
    await db.users.insert_one(user_data)
    return user_data

@pytest_asyncio.fixture
async def another_user(db):
    """Create another test user."""
    user_data = {
        "_id": ObjectId(),
        "email": "anotheruser@example.com",
        "full_name": "Another User",
        "phone": "9876543210",
        "location": {
            "address": "456 Another St",
            "city": "Test City",
            "state": "TS",
            "zip_code": "12345"
        },
        "stats": {
            "average_rating": 4.0,
            "total_reviews": 5
        },
        "role": UserRole.USER,
        "status": AccountStatus.ACTIVE,
        "verified": True,
        "created_at": datetime.utcnow()
    }
    await db.users.insert_one(user_data)
    return user_data

@pytest.fixture
def override_get_db(db):
    """Override the get_database dependency."""
    async def _override_get_db():
        return db
    return _override_get_db

@pytest.fixture
def override_current_user(test_user):
    """Override the get_current_user dependency."""
    async def _override_current_user():
        return test_user
    return _override_current_user

@pytest_asyncio.fixture
async def client(override_get_db, override_current_user):
    """Create test client with overridden dependencies."""
    from app.database import get_database
    from app.dependencies import get_current_user
    
    app.dependency_overrides[get_database] = override_get_db
    app.dependency_overrides[get_current_user] = override_current_user
    
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
    
    app.dependency_overrides.clear()

@pytest.fixture
def meal_create_data():
    """Sample meal creation data."""
    return {
        "title": "Delicious Pasta Carbonara",
        "description": "Authentic Italian pasta with creamy sauce and bacon",
        "cuisine_type": "Italian",
        "meal_type": "dinner",
        "photos": ["http://example.com/photo1.jpg"],
        "allergen_info": {
            "contains": ["dairy", "eggs"],
            "may_contain": ["gluten"]
        },
        "nutrition_info": {
            "calories": 650,
            "protein_grams": 25.0,
            "carbs_grams": 60.0,
            "fat_grams": 30.0
        },
        "portion_size": "Serves 2",
        "available_for_sale": True,
        "sale_price": 15.99,
        "available_for_swap": False,
        "swap_preferences": [],
        "preparation_date": datetime.utcnow().isoformat(),
        "expires_date": (datetime.utcnow() + timedelta(days=2)).isoformat(),
        "pickup_instructions": "Ring doorbell at front door"
    }


# ============================================================
# CREATE MEAL TESTS
# ============================================================

@pytest.mark.asyncio
async def test_create_meal_success(client, meal_create_data, db):
    """Test successful meal creation."""
    response = await client.post("/api/meals/", json=meal_create_data)
    
    assert response.status_code == 201
    data = response.json()
    
    assert data["title"] == meal_create_data["title"]
    assert data["description"] == meal_create_data["description"]
    assert data["cuisine_type"] == meal_create_data["cuisine_type"]
    assert data["sale_price"] == meal_create_data["sale_price"]
    assert data["status"] == MealStatus.AVAILABLE
    assert "id" in data
    assert "seller_id" in data
    assert "seller_name" in data
    assert data["average_rating"] == 0.0
    assert data["total_reviews"] == 0
    assert data["views"] == 0
    
    # Verify meal in database
    meal = await db.meals.find_one({"_id": ObjectId(data["id"])})
    assert meal is not None
    assert meal["title"] == meal_create_data["title"]

@pytest.mark.asyncio
async def test_create_meal_for_swap_only(client, meal_create_data):
    """Test creating a meal available only for swap."""
    meal_create_data["available_for_sale"] = False
    meal_create_data["sale_price"] = None
    meal_create_data["available_for_swap"] = True
    meal_create_data["swap_preferences"] = ["Asian cuisine", "Desserts"]
    
    response = await client.post("/api/meals/", json=meal_create_data)
    
    assert response.status_code == 201
    data = response.json()
    
    assert data["available_for_sale"] is False
    assert data["sale_price"] is None
    assert data["available_for_swap"] is True
    assert data["swap_preferences"] == ["Asian cuisine", "Desserts"]


# ============================================================
# GET MEALS TESTS
# ============================================================

@pytest.mark.asyncio
async def test_get_all_meals(client, db, test_user, another_user):
    """Test getting all available meals."""
    # Create multiple meals
    meals = [
        {
            "seller_id": test_user["_id"],
            "title": "Pasta Carbonara",
            "description": "Italian pasta dish",
            "cuisine_type": "Italian",
            "meal_type": "dinner",
            "photos": [],
            "allergen_info": {"contains": ["dairy"], "may_contain": []},
            "portion_size": "Serves 2",
            "available_for_sale": True,
            "sale_price": 15.99,
            "available_for_swap": False,
            "swap_preferences": [],
            "status": MealStatus.AVAILABLE,
            "preparation_date": datetime.utcnow(),
            "expires_date": datetime.utcnow() + timedelta(days=2),
            "average_rating": 0.0,
            "total_reviews": 0,
            "views": 0,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "seller_id": another_user["_id"],
            "title": "Chicken Tacos",
            "description": "Mexican style tacos",
            "cuisine_type": "Mexican",
            "meal_type": "lunch",
            "photos": [],
            "allergen_info": {"contains": [], "may_contain": []},
            "portion_size": "Serves 3",
            "available_for_sale": True,
            "sale_price": 12.99,
            "available_for_swap": True,
            "swap_preferences": ["Italian"],
            "status": MealStatus.AVAILABLE,
            "preparation_date": datetime.utcnow(),
            "expires_date": datetime.utcnow() + timedelta(days=1),
            "average_rating": 0.0,
            "total_reviews": 0,
            "views": 0,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
    ]
    await db.meals.insert_many(meals)
    
    response = await client.get("/api/meals/")
    
    assert response.status_code == 200
    data = response.json()
    
    assert len(data) == 2
    assert any(m["title"] == "Pasta Carbonara" for m in data)
    assert any(m["title"] == "Chicken Tacos" for m in data)

@pytest.mark.asyncio
async def test_get_meals_with_cuisine_filter(client, db, test_user):
    """Test filtering meals by cuisine type."""
    meals = [
        {
            "seller_id": test_user["_id"],
            "title": "Pasta",
            "description": "Italian pasta",
            "cuisine_type": "Italian",
            "meal_type": "dinner",
            "photos": [],
            "allergen_info": {"contains": [], "may_contain": []},
            "portion_size": "Serves 2",
            "available_for_sale": True,
            "sale_price": 15.99,
            "available_for_swap": False,
            "swap_preferences": [],
            "status": MealStatus.AVAILABLE,
            "preparation_date": datetime.utcnow(),
            "expires_date": datetime.utcnow() + timedelta(days=2),
            "average_rating": 0.0,
            "total_reviews": 0,
            "views": 0,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "seller_id": test_user["_id"],
            "title": "Tacos",
            "description": "Mexican tacos",
            "cuisine_type": "Mexican",
            "meal_type": "lunch",
            "photos": [],
            "allergen_info": {"contains": [], "may_contain": []},
            "portion_size": "Serves 3",
            "available_for_sale": True,
            "sale_price": 12.99,
            "available_for_swap": False,
            "swap_preferences": [],
            "status": MealStatus.AVAILABLE,
            "preparation_date": datetime.utcnow(),
            "expires_date": datetime.utcnow() + timedelta(days=1),
            "average_rating": 0.0,
            "total_reviews": 0,
            "views": 0,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
    ]
    await db.meals.insert_many(meals)
    
    response = await client.get("/api/meals/?cuisine_type=Italian")
    
    assert response.status_code == 200
    data = response.json()
    
    assert len(data) == 1
    assert data[0]["cuisine_type"] == "Italian"
    assert data[0]["title"] == "Pasta"

@pytest.mark.asyncio
async def test_get_meals_with_price_filter(client, db, test_user):
    """Test filtering meals by maximum price."""
    meals = [
        {
            "seller_id": test_user["_id"],
            "title": "Expensive Meal",
            "description": "Costly dish",
            "cuisine_type": "French",
            "meal_type": "dinner",
            "photos": [],
            "allergen_info": {"contains": [], "may_contain": []},
            "portion_size": "Serves 1",
            "available_for_sale": True,
            "sale_price": 50.00,
            "available_for_swap": False,
            "swap_preferences": [],
            "status": MealStatus.AVAILABLE,
            "preparation_date": datetime.utcnow(),
            "expires_date": datetime.utcnow() + timedelta(days=1),
            "average_rating": 0.0,
            "total_reviews": 0,
            "views": 0,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "seller_id": test_user["_id"],
            "title": "Budget Meal",
            "description": "Affordable dish",
            "cuisine_type": "American",
            "meal_type": "lunch",
            "photos": [],
            "allergen_info": {"contains": [], "may_contain": []},
            "portion_size": "Serves 2",
            "available_for_sale": True,
            "sale_price": 10.00,
            "available_for_swap": False,
            "swap_preferences": [],
            "status": MealStatus.AVAILABLE,
            "preparation_date": datetime.utcnow(),
            "expires_date": datetime.utcnow() + timedelta(days=1),
            "average_rating": 0.0,
            "total_reviews": 0,
            "views": 0,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
    ]
    await db.meals.insert_many(meals)
    
    response = await client.get("/api/meals/?max_price=20.00")
    
    assert response.status_code == 200
    data = response.json()
    
    assert len(data) == 1
    assert data[0]["title"] == "Budget Meal"
    assert data[0]["sale_price"] <= 20.00

@pytest.mark.asyncio
async def test_get_meals_pagination(client, db, test_user):
    """Test meal pagination."""
    # Create 25 meals
    meals = []
    for i in range(25):
        meals.append({
            "seller_id": test_user["_id"],
            "title": f"Meal {i}",
            "description": f"Description {i}",
            "cuisine_type": "Italian",
            "meal_type": "dinner",
            "photos": [],
            "allergen_info": {"contains": [], "may_contain": []},
            "portion_size": "Serves 1",
            "available_for_sale": True,
            "sale_price": 10.00,
            "available_for_swap": False,
            "swap_preferences": [],
            "status": MealStatus.AVAILABLE,
            "preparation_date": datetime.utcnow(),
            "expires_date": datetime.utcnow() + timedelta(days=1),
            "average_rating": 0.0,
            "total_reviews": 0,
            "views": 0,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        })
    await db.meals.insert_many(meals)
    
    # Get first page
    response = await client.get("/api/meals/?skip=0&limit=10")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 10
    
    # Get second page
    response = await client.get("/api/meals/?skip=10&limit=10")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 10
    
    # Get third page
    response = await client.get("/api/meals/?skip=20&limit=10")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 5


# ============================================================
# GET MEAL BY ID TESTS
# ============================================================

@pytest.mark.asyncio
async def test_get_meal_by_id_success(client, db, test_user):
    """Test getting a specific meal by ID."""
    meal = {
        "_id": ObjectId(),
        "seller_id": test_user["_id"],
        "title": "Test Meal",
        "description": "Test description",
        "cuisine_type": "Italian",
        "meal_type": "dinner",
        "photos": [],
        "allergen_info": {"contains": [], "may_contain": []},
        "portion_size": "Serves 2",
        "available_for_sale": True,
        "sale_price": 15.99,
        "available_for_swap": False,
        "swap_preferences": [],
        "status": MealStatus.AVAILABLE,
        "preparation_date": datetime.utcnow(),
        "expires_date": datetime.utcnow() + timedelta(days=2),
        "average_rating": 0.0,
        "total_reviews": 0,
        "views": 5,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    await db.meals.insert_one(meal)
    
    response = await client.get(f"/api/meals/{str(meal['_id'])}")
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["id"] == str(meal["_id"])
    assert data["title"] == "Test Meal"
    assert data["views"] == 6  # Should be incremented
    
    # Verify views were incremented in database
    updated_meal = await db.meals.find_one({"_id": meal["_id"]})
    assert updated_meal["views"] == 6

@pytest.mark.asyncio
async def test_get_meal_by_id_not_found(client):
    """Test getting a non-existent meal."""
    fake_id = str(ObjectId())
    response = await client.get(f"/api/meals/{fake_id}")
    
    assert response.status_code == 404
    assert "Meal not found" in response.json()["detail"]

@pytest.mark.asyncio
async def test_get_meal_by_invalid_id(client):
    """Test getting a meal with invalid ID format."""
    response = await client.get("/api/meals/invalid-id")
    
    assert response.status_code == 400
    assert "Invalid meal ID" in response.json()["detail"]


# ============================================================
# GET MY MEALS TESTS
# ============================================================

@pytest.mark.asyncio
async def test_get_my_meals(client, db, test_user, another_user):
    """Test getting meals created by authenticated user."""
    # Create meals for both users
    my_meals = [
        {
            "seller_id": test_user["_id"],
            "title": "My Meal 1",
            "description": "Description 1",
            "cuisine_type": "Italian",
            "meal_type": "dinner",
            "photos": [],
            "allergen_info": {"contains": [], "may_contain": []},
            "portion_size": "Serves 2",
            "available_for_sale": True,
            "sale_price": 15.99,
            "available_for_swap": False,
            "swap_preferences": [],
            "status": MealStatus.AVAILABLE,
            "preparation_date": datetime.utcnow(),
            "expires_date": datetime.utcnow() + timedelta(days=2),
            "average_rating": 0.0,
            "total_reviews": 0,
            "views": 0,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "seller_id": test_user["_id"],
            "title": "My Meal 2",
            "description": "Description 2",
            "cuisine_type": "Mexican",
            "meal_type": "lunch",
            "photos": [],
            "allergen_info": {"contains": [], "may_contain": []},
            "portion_size": "Serves 1",
            "available_for_sale": True,
            "sale_price": 10.99,
            "available_for_swap": False,
            "swap_preferences": [],
            "status": MealStatus.SOLD,
            "preparation_date": datetime.utcnow(),
            "expires_date": datetime.utcnow() + timedelta(days=1),
            "average_rating": 0.0,
            "total_reviews": 0,
            "views": 0,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
    ]
    other_meal = {
        "seller_id": another_user["_id"],
        "title": "Other User Meal",
        "description": "Not my meal",
        "cuisine_type": "Asian",
        "meal_type": "dinner",
        "photos": [],
        "allergen_info": {"contains": [], "may_contain": []},
        "portion_size": "Serves 2",
        "available_for_sale": True,
        "sale_price": 20.00,
        "available_for_swap": False,
        "swap_preferences": [],
        "status": MealStatus.AVAILABLE,
        "preparation_date": datetime.utcnow(),
        "expires_date": datetime.utcnow() + timedelta(days=2),
        "average_rating": 0.0,
        "total_reviews": 0,
        "views": 0,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    
    await db.meals.insert_many(my_meals + [other_meal])
    
    response = await client.get("/api/meals/my/listings")
    
    assert response.status_code == 200
    data = response.json()
    
    assert len(data) == 2
    assert all(m["seller_id"] == str(test_user["_id"]) for m in data)
    assert any(m["title"] == "My Meal 1" for m in data)
    assert any(m["title"] == "My Meal 2" for m in data)
    assert not any(m["title"] == "Other User Meal" for m in data)


# ============================================================
# UPDATE MEAL TESTS
# ============================================================

@pytest.mark.asyncio
async def test_update_meal_success(client, db, test_user):
    """Test successfully updating a meal."""
    meal = {
        "_id": ObjectId(),
        "seller_id": test_user["_id"],
        "title": "Original Title",
        "description": "Original description",
        "cuisine_type": "Italian",
        "meal_type": "dinner",
        "photos": [],
        "allergen_info": {"contains": ["dairy"], "may_contain": []},
        "portion_size": "Serves 2",
        "available_for_sale": True,
        "sale_price": 15.99,
        "available_for_swap": False,
        "swap_preferences": [],
        "status": MealStatus.AVAILABLE,
        "preparation_date": datetime.utcnow(),
        "expires_date": datetime.utcnow() + timedelta(days=2),
        "average_rating": 0.0,
        "total_reviews": 0,
        "views": 0,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    await db.meals.insert_one(meal)
    
    update_data = {
        "title": "Updated Title",
        "sale_price": 19.99,
        "status": MealStatus.UNAVAILABLE
    }
    
    response = await client.put(f"/api/meals/{str(meal['_id'])}", json=update_data)
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["title"] == "Updated Title"
    assert data["sale_price"] == 19.99
    assert data["status"] == MealStatus.UNAVAILABLE
    assert data["description"] == "Original description"  # Unchanged

@pytest.mark.asyncio
async def test_update_meal_not_owner(client, db, another_user):
    """Test updating a meal that belongs to another user."""
    meal = {
        "_id": ObjectId(),
        "seller_id": another_user["_id"],
        "title": "Another User's Meal",
        "description": "Description",
        "cuisine_type": "Italian",
        "meal_type": "dinner",
        "photos": [],
        "allergen_info": {"contains": [], "may_contain": []},
        "portion_size": "Serves 2",
        "available_for_sale": True,
        "sale_price": 15.99,
        "available_for_swap": False,
        "swap_preferences": [],
        "status": MealStatus.AVAILABLE,
        "preparation_date": datetime.utcnow(),
        "expires_date": datetime.utcnow() + timedelta(days=2),
        "average_rating": 0.0,
        "total_reviews": 0,
        "views": 0,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    await db.meals.insert_one(meal)
    
    update_data = {"title": "Hacked Title"}
    
    response = await client.put(f"/api/meals/{str(meal['_id'])}", json=update_data)
    
    assert response.status_code == 403
    assert "permission" in response.json()["detail"].lower()

@pytest.mark.asyncio
async def test_update_meal_not_found(client):
    """Test updating a non-existent meal."""
    fake_id = str(ObjectId())
    update_data = {"title": "New Title"}
    
    response = await client.put(f"/api/meals/{fake_id}", json=update_data)
    
    assert response.status_code == 404
    assert "Meal not found" in response.json()["detail"]


# ============================================================
# DELETE MEAL TESTS
# ============================================================

@pytest.mark.asyncio
async def test_delete_meal_success(client, db, test_user):
    """Test successfully deleting a meal."""
    meal = {
        "_id": ObjectId(),
        "seller_id": test_user["_id"],
        "title": "Meal to Delete",
        "description": "Description",
        "cuisine_type": "Italian",
        "meal_type": "dinner",
        "photos": [],
        "allergen_info": {"contains": [], "may_contain": []},
        "portion_size": "Serves 2",
        "available_for_sale": True,
        "sale_price": 15.99,
        "available_for_swap": False,
        "swap_preferences": [],
        "status": MealStatus.AVAILABLE,
        "preparation_date": datetime.utcnow(),
        "expires_date": datetime.utcnow() + timedelta(days=2),
        "average_rating": 0.0,
        "total_reviews": 0,
        "views": 0,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    await db.meals.insert_one(meal)
    
    response = await client.delete(f"/api/meals/{str(meal['_id'])}")
    
    assert response.status_code == 200
    assert "successfully deleted" in response.json()["message"].lower()
    
    # Verify meal is deleted from database
    deleted_meal = await db.meals.find_one({"_id": meal["_id"]})
    assert deleted_meal is None

@pytest.mark.asyncio
async def test_delete_meal_not_owner(client, db, another_user):
    """Test deleting a meal that belongs to another user."""
    meal = {
        "_id": ObjectId(),
        "seller_id": another_user["_id"],
        "title": "Another User's Meal",
        "description": "Description",
        "cuisine_type": "Italian",
        "meal_type": "dinner",
        "photos": [],
        "allergen_info": {"contains": [], "may_contain": []},
        "portion_size": "Serves 2",
        "available_for_sale": True,
        "sale_price": 15.99,
        "available_for_swap": False,
        "swap_preferences": [],
        "status": MealStatus.AVAILABLE,
        "preparation_date": datetime.utcnow(),
        "expires_date": datetime.utcnow() + timedelta(days=2),
        "average_rating": 0.0,
        "total_reviews": 0,
        "views": 0,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    await db.meals.insert_one(meal)
    
    response = await client.delete(f"/api/meals/{str(meal['_id'])}")
    
    assert response.status_code == 403
    assert "permission" in response.json()["detail"].lower()
    
    # Verify meal still exists
    existing_meal = await db.meals.find_one({"_id": meal["_id"]})
    assert existing_meal is not None

@pytest.mark.asyncio
async def test_delete_meal_not_found(client):
    """Test deleting a non-existent meal."""
    fake_id = str(ObjectId())
    
    response = await client.delete(f"/api/meals/{fake_id}")
    
    assert response.status_code == 404
    assert "Meal not found" in response.json()["detail"]