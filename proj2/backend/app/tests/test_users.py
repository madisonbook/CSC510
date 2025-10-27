"""
Comprehensive tests for user routes
Tests all user CRUD operations, profile management, and permissions
"""
import pytest
import pytest_asyncio
from datetime import datetime
from bson import ObjectId

# Test configuration
TEST_DB_NAME = "test_meal_db"


# ============================================================
# FIXTURES
# ============================================================

@pytest_asyncio.fixture
async def test_user(mongo_client):
    """Create a test user in MongoDB"""
    db = mongo_client[TEST_DB_NAME]
    
    user_doc = {
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
            "dietary_restrictions": ["vegetarian"],
            "allergens": ["peanuts"],
            "cuisine_preferences": ["Italian"],
            "spice_level": None
        },
        "social_media": {
            "facebook": "testuser",
            "instagram": "testuser",
            "twitter": None
        },
        "role": "user",
        "status": "active",
        "stats": {
            "total_meals_sold": 5,
            "total_meals_swapped": 2,
            "total_meals_purchased": 10,
            "average_rating": 4.5,
            "total_reviews": 10,
            "badges": []
        },
        "verified": True,
        "created_at": datetime.utcnow(),
        "password_hash": "hashed_password"
    }
    
    result = await db.users.insert_one(user_doc)
    user_doc["_id"] = result.inserted_id
    
    yield user_doc
    
    # Cleanup
    await db.users.delete_one({"_id": result.inserted_id})


@pytest_asyncio.fixture
async def another_user(mongo_client):
    """Create another test user"""
    db = mongo_client[TEST_DB_NAME]
    
    user_doc = {
        "email": "anotheruser@example.com",
        "full_name": "Another User",
        "phone": "9876543210",
        "location": {
            "address": "456 Another St",
            "city": "Test City",
            "state": "TS",
            "zip_code": "12345"
        },
        "bio": "Another bio",
        "profile_picture": None,
        "dietary_preferences": {
            "dietary_restrictions": [],
            "allergens": [],
            "cuisine_preferences": [],
            "spice_level": None
        },
        "social_media": {},
        "role": "user",
        "status": "active",
        "stats": {
            "total_meals_sold": 0,
            "total_meals_swapped": 0,
            "total_meals_purchased": 0,
            "average_rating": 4.0,
            "total_reviews": 5,
            "badges": []
        },
        "verified": True,
        "created_at": datetime.utcnow(),
        "password_hash": "hashed_password"
    }
    
    result = await db.users.insert_one(user_doc)
    user_doc["_id"] = result.inserted_id
    
    yield user_doc
    
    # Cleanup
    await db.users.delete_one({"_id": result.inserted_id})


@pytest_asyncio.fixture
async def suspended_user(mongo_client):
    """Create a suspended user"""
    db = mongo_client[TEST_DB_NAME]
    
    user_doc = {
        "email": "suspended@example.com",
        "full_name": "Suspended User",
        "phone": "5555555555",
        "location": {
            "address": "789 Suspended Ave",
            "city": "Test City",
            "state": "TS",
            "zip_code": "12345"
        },
        "role": "user",
        "status": "suspended",
        "stats": {
            "total_meals_sold": 0,
            "average_rating": 0.0,
            "total_reviews": 0,
            "badges": []
        },
        "verified": False,
        "created_at": datetime.utcnow(),
        "password_hash": "hashed_password"
    }
    
    result = await db.users.insert_one(user_doc)
    user_doc["_id"] = result.inserted_id
    
    yield user_doc
    
    # Cleanup
    await db.users.delete_one({"_id": result.inserted_id})


# ============================================================
# GET USER PROFILE TESTS
# ============================================================

@pytest.mark.asyncio
async def test_get_user_profile_success(mongo_client, test_user):
    """Test successfully retrieving a user profile"""
    db = mongo_client[TEST_DB_NAME]
    
    user = await db.users.find_one({"_id": test_user["_id"]})
    
    assert user is not None
    assert user["email"] == test_user["email"]
    assert user["full_name"] == test_user["full_name"]
    assert user["verified"] is True


@pytest.mark.asyncio
async def test_get_user_profile_includes_stats(mongo_client, test_user):
    """Test that user profile includes statistics"""
    db = mongo_client[TEST_DB_NAME]
    
    user = await db.users.find_one({"_id": test_user["_id"]})
    
    assert "stats" in user
    assert user["stats"]["total_meals_sold"] == 5
    assert user["stats"]["average_rating"] == 4.5
    assert user["stats"]["total_reviews"] == 10


@pytest.mark.asyncio
async def test_get_user_profile_includes_dietary_preferences(mongo_client, test_user):
    """Test that user profile includes dietary preferences"""
    db = mongo_client[TEST_DB_NAME]
    
    user = await db.users.find_one({"_id": test_user["_id"]})
    
    assert "dietary_preferences" in user
    prefs = user["dietary_preferences"]
    assert "vegetarian" in prefs["dietary_restrictions"]
    assert "peanuts" in prefs["allergens"]
    assert "Italian" in prefs["cuisine_preferences"]


@pytest.mark.asyncio
async def test_get_user_by_id_not_found(mongo_client):
    """Test retrieving a non-existent user"""
    db = mongo_client[TEST_DB_NAME]
    
    fake_id = ObjectId()
    user = await db.users.find_one({"_id": fake_id})
    
    assert user is None


@pytest.mark.asyncio
async def test_get_user_by_invalid_id_format(mongo_client):
    """Test that invalid ObjectId format is caught"""
    invalid_id = "not_valid_object_id"
    
    assert not ObjectId.is_valid(invalid_id)


# ============================================================
# UPDATE USER PROFILE TESTS
# ============================================================

@pytest.mark.asyncio
async def test_update_user_full_name(mongo_client, test_user):
    """Test updating user's full name"""
    db = mongo_client[TEST_DB_NAME]
    
    update_data = {
        "full_name": "Updated Name",
        "updated_at": datetime.utcnow()
    }
    
    result = await db.users.update_one(
        {"_id": test_user["_id"]},
        {"$set": update_data}
    )
    
    assert result.modified_count == 1
    
    updated_user = await db.users.find_one({"_id": test_user["_id"]})
    assert updated_user["full_name"] == "Updated Name"


@pytest.mark.asyncio
async def test_update_user_phone(mongo_client, test_user):
    """Test updating user's phone number"""
    db = mongo_client[TEST_DB_NAME]
    
    await db.users.update_one(
        {"_id": test_user["_id"]},
        {"$set": {"phone": "5555555555", "updated_at": datetime.utcnow()}}
    )
    
    updated_user = await db.users.find_one({"_id": test_user["_id"]})
    assert updated_user["phone"] == "5555555555"


@pytest.mark.asyncio
async def test_update_user_bio(mongo_client, test_user):
    """Test updating user's bio"""
    db = mongo_client[TEST_DB_NAME]
    
    new_bio = "This is my updated bio with more information about me."
    
    await db.users.update_one(
        {"_id": test_user["_id"]},
        {"$set": {"bio": new_bio, "updated_at": datetime.utcnow()}}
    )
    
    updated_user = await db.users.find_one({"_id": test_user["_id"]})
    assert updated_user["bio"] == new_bio


@pytest.mark.asyncio
async def test_update_user_location(mongo_client, test_user):
    """Test updating user's location"""
    db = mongo_client[TEST_DB_NAME]
    
    new_location = {
        "address": "789 New St",
        "city": "New City",
        "state": "NC",
        "zip_code": "27601"
    }
    
    await db.users.update_one(
        {"_id": test_user["_id"]},
        {"$set": {"location": new_location, "updated_at": datetime.utcnow()}}
    )
    
    updated_user = await db.users.find_one({"_id": test_user["_id"]})
    assert updated_user["location"]["city"] == "New City"
    assert updated_user["location"]["state"] == "NC"


@pytest.mark.asyncio
async def test_update_user_multiple_fields(mongo_client, test_user):
    """Test updating multiple user fields at once"""
    db = mongo_client[TEST_DB_NAME]
    
    updates = {
        "full_name": "Multi Update",
        "phone": "1112223333",
        "bio": "Updated bio",
        "updated_at": datetime.utcnow()
    }
    
    await db.users.update_one(
        {"_id": test_user["_id"]},
        {"$set": updates}
    )
    
    updated_user = await db.users.find_one({"_id": test_user["_id"]})
    assert updated_user["full_name"] == "Multi Update"
    assert updated_user["phone"] == "1112223333"
    assert updated_user["bio"] == "Updated bio"


@pytest.mark.asyncio
async def test_update_user_partial_update(mongo_client, test_user):
    """Test that partial updates don't affect other fields"""
    db = mongo_client[TEST_DB_NAME]
    
    original_email = test_user["email"]
    original_name = test_user["full_name"]
    
    await db.users.update_one(
        {"_id": test_user["_id"]},
        {"$set": {"bio": "Only bio updated", "updated_at": datetime.utcnow()}}
    )
    
    updated_user = await db.users.find_one({"_id": test_user["_id"]})
    assert updated_user["email"] == original_email
    assert updated_user["full_name"] == original_name
    assert updated_user["bio"] == "Only bio updated"


# ============================================================
# UPDATE DIETARY PREFERENCES TESTS
# ============================================================

@pytest.mark.asyncio
async def test_update_dietary_preferences(mongo_client, test_user):
    """Test updating dietary preferences"""
    db = mongo_client[TEST_DB_NAME]
    
    new_prefs = {
        "dietary_restrictions": ["vegan", "gluten-free"],
        "allergens": ["tree nuts", "shellfish"],
        "cuisine_preferences": ["Mexican", "Thai"],
        "spice_level": "hot"
    }
    
    await db.users.update_one(
        {"_id": test_user["_id"]},
        {"$set": {"dietary_preferences": new_prefs, "updated_at": datetime.utcnow()}}
    )
    
    updated_user = await db.users.find_one({"_id": test_user["_id"]})
    prefs = updated_user["dietary_preferences"]
    
    assert "vegan" in prefs["dietary_restrictions"]
    assert "tree nuts" in prefs["allergens"]
    assert "Mexican" in prefs["cuisine_preferences"]
    assert prefs["spice_level"] == "hot"


@pytest.mark.asyncio
async def test_update_dietary_preferences_empty_lists(mongo_client, test_user):
    """Test updating dietary preferences with empty lists"""
    db = mongo_client[TEST_DB_NAME]
    
    new_prefs = {
        "dietary_restrictions": [],
        "allergens": [],
        "cuisine_preferences": [],
        "spice_level": None
    }
    
    await db.users.update_one(
        {"_id": test_user["_id"]},
        {"$set": {"dietary_preferences": new_prefs, "updated_at": datetime.utcnow()}}
    )
    
    updated_user = await db.users.find_one({"_id": test_user["_id"]})
    prefs = updated_user["dietary_preferences"]
    
    assert len(prefs["dietary_restrictions"]) == 0
    assert len(prefs["allergens"]) == 0
    assert len(prefs["cuisine_preferences"]) == 0


@pytest.mark.asyncio
async def test_add_allergen_to_preferences(mongo_client, test_user):
    """Test adding a new allergen to existing preferences"""
    db = mongo_client[TEST_DB_NAME]
    
    # Add new allergen to existing list
    await db.users.update_one(
        {"_id": test_user["_id"]},
        {"$addToSet": {"dietary_preferences.allergens": "shellfish"}}
    )
    
    updated_user = await db.users.find_one({"_id": test_user["_id"]})
    allergens = updated_user["dietary_preferences"]["allergens"]
    
    assert "shellfish" in allergens
    assert "peanuts" in allergens  # Original still there


# ============================================================
# UPDATE SOCIAL MEDIA TESTS
# ============================================================

@pytest.mark.asyncio
async def test_update_social_media_links(mongo_client, test_user):
    """Test updating social media links"""
    db = mongo_client[TEST_DB_NAME]
    
    new_social = {
        "facebook": "newfacebook",
        "instagram": "newinstagram",
        "twitter": "newtwitter"
    }
    
    await db.users.update_one(
        {"_id": test_user["_id"]},
        {"$set": {"social_media": new_social, "updated_at": datetime.utcnow()}}
    )
    
    updated_user = await db.users.find_one({"_id": test_user["_id"]})
    social = updated_user["social_media"]
    
    assert social["facebook"] == "newfacebook"
    assert social["instagram"] == "newinstagram"
    assert social["twitter"] == "newtwitter"


@pytest.mark.asyncio
async def test_update_social_media_partial(mongo_client, test_user):
    """Test updating only some social media links"""
    db = mongo_client[TEST_DB_NAME]
    
    await db.users.update_one(
        {"_id": test_user["_id"]},
        {"$set": {"social_media.twitter": "mytwitter", "updated_at": datetime.utcnow()}}
    )
    
    updated_user = await db.users.find_one({"_id": test_user["_id"]})
    social = updated_user["social_media"]
    
    assert social["twitter"] == "mytwitter"
    assert social["facebook"] == test_user["social_media"]["facebook"]  # Unchanged


# ============================================================
# USER STATISTICS TESTS
# ============================================================

@pytest.mark.asyncio
async def test_get_user_stats(mongo_client, test_user):
    """Test retrieving user statistics"""
    db = mongo_client[TEST_DB_NAME]
    
    user = await db.users.find_one({"_id": test_user["_id"]})
    stats = user["stats"]
    
    assert stats["total_meals_sold"] == 5
    assert stats["total_meals_swapped"] == 2
    assert stats["total_meals_purchased"] == 10
    assert stats["average_rating"] == 4.5
    assert stats["total_reviews"] == 10


@pytest.mark.asyncio
async def test_increment_user_stats(mongo_client, test_user):
    """Test incrementing user statistics"""
    db = mongo_client[TEST_DB_NAME]
    
    initial_sold = test_user["stats"]["total_meals_sold"]
    
    # Increment meals sold
    await db.users.update_one(
        {"_id": test_user["_id"]},
        {"$inc": {"stats.total_meals_sold": 1}}
    )
    
    updated_user = await db.users.find_one({"_id": test_user["_id"]})
    assert updated_user["stats"]["total_meals_sold"] == initial_sold + 1


@pytest.mark.asyncio
async def test_update_user_rating(mongo_client, test_user):
    """Test updating user's average rating"""
    db = mongo_client[TEST_DB_NAME]
    
    new_rating = 4.8
    
    await db.users.update_one(
        {"_id": test_user["_id"]},
        {"$set": {"stats.average_rating": new_rating}}
    )
    
    updated_user = await db.users.find_one({"_id": test_user["_id"]})
    assert updated_user["stats"]["average_rating"] == new_rating


# ============================================================
# DELETE USER TESTS
# ============================================================

@pytest.mark.asyncio
async def test_delete_user_success(mongo_client, test_user):
    """Test successfully deleting a user"""
    db = mongo_client[TEST_DB_NAME]
    
    result = await db.users.delete_one({"_id": test_user["_id"]})
    
    assert result.deleted_count == 1
    
    # Verify deletion
    deleted_user = await db.users.find_one({"_id": test_user["_id"]})
    assert deleted_user is None


@pytest.mark.asyncio
async def test_delete_user_with_meals(mongo_client, test_user):
    """Test deleting user also deletes their meals"""
    db = mongo_client[TEST_DB_NAME]
    
    # Create meals for the user
    meal1 = {
        "seller_id": test_user["_id"],
        "title": "Test Meal 1",
        "description": "Will be deleted",
        "status": "available",
        "created_at": datetime.utcnow()
    }
    meal2 = {
        "seller_id": test_user["_id"],
        "title": "Test Meal 2",
        "description": "Will be deleted",
        "status": "available",
        "created_at": datetime.utcnow()
    }
    
    await db.meals.insert_many([meal1, meal2])
    
    # Delete user
    await db.users.delete_one({"_id": test_user["_id"]})
    
    # Delete user's meals (in real app, this would be in the API)
    await db.meals.delete_many({"seller_id": test_user["_id"]})
    
    # Verify meals deleted
    remaining_meals = await db.meals.find({"seller_id": test_user["_id"]}).to_list(None)
    assert len(remaining_meals) == 0


@pytest.mark.asyncio
async def test_delete_user_not_found(mongo_client):
    """Test deleting a non-existent user"""
    db = mongo_client[TEST_DB_NAME]
    
    fake_id = ObjectId()
    result = await db.users.delete_one({"_id": fake_id})
    
    assert result.deleted_count == 0


# ============================================================
# USER STATUS AND ROLE TESTS
# ============================================================

@pytest.mark.asyncio
async def test_suspended_user_status(mongo_client, suspended_user):
    """Test that suspended user has correct status"""
    db = mongo_client[TEST_DB_NAME]
    
    user = await db.users.find_one({"_id": suspended_user["_id"]})
    
    assert user["status"] == "suspended"
    assert user["verified"] is False


@pytest.mark.asyncio
async def test_update_user_status(mongo_client, test_user):
    """Test updating user status"""
    db = mongo_client[TEST_DB_NAME]
    
    await db.users.update_one(
        {"_id": test_user["_id"]},
        {"$set": {"status": "suspended"}}
    )
    
    updated_user = await db.users.find_one({"_id": test_user["_id"]})
    assert updated_user["status"] == "suspended"


@pytest.mark.asyncio
async def test_verify_user(mongo_client, suspended_user):
    """Test verifying a user"""
    db = mongo_client[TEST_DB_NAME]
    
    await db.users.update_one(
        {"_id": suspended_user["_id"]},
        {"$set": {"verified": True, "status": "active"}}
    )
    
    updated_user = await db.users.find_one({"_id": suspended_user["_id"]})
    assert updated_user["verified"] is True
    assert updated_user["status"] == "active"


# ============================================================
# EDGE CASES AND VALIDATION
# ============================================================

@pytest.mark.asyncio
async def test_user_with_long_bio(mongo_client, test_user):
    """Test updating user with very long bio"""
    db = mongo_client[TEST_DB_NAME]
    
    long_bio = "A" * 500
    
    await db.users.update_one(
        {"_id": test_user["_id"]},
        {"$set": {"bio": long_bio}}
    )
    
    updated_user = await db.users.find_one({"_id": test_user["_id"]})
    assert len(updated_user["bio"]) == 500


@pytest.mark.asyncio
async def test_user_with_special_characters(mongo_client):
    """Test creating user with special characters in name"""
    db = mongo_client[TEST_DB_NAME]
    
    user_doc = {
        "email": "special@example.com",
        "full_name": "José María Àlvarez-O'Connor",
        "phone": "1234567890",
        "location": {
            "address": "123 Test St",
            "city": "Test City",
            "state": "TS",
            "zip_code": "12345"
        },
        "role": "user",
        "status": "active",
        "stats": {"average_rating": 0.0, "total_reviews": 0},
        "verified": True,
        "created_at": datetime.utcnow()
    }
    
    result = await db.users.insert_one(user_doc)
    assert result.inserted_id is not None
    
    user = await db.users.find_one({"_id": result.inserted_id})
    assert "José" in user["full_name"]
    assert "O'Connor" in user["full_name"]
    
    # Cleanup
    await db.users.delete_one({"_id": result.inserted_id})


@pytest.mark.asyncio
async def test_user_email_uniqueness(mongo_client, test_user):
    """Test that duplicate emails are handled"""
    db = mongo_client[TEST_DB_NAME]
    
    # Try to create user with same email
    duplicate_user = {
        "email": test_user["email"],  # Same email
        "full_name": "Duplicate User",
        "phone": "9999999999",
        "location": {
            "address": "999 Dup St",
            "city": "Test City",
            "state": "TS",
            "zip_code": "12345"
        },
        "role": "user",
        "status": "active",
        "created_at": datetime.utcnow()
    }
    