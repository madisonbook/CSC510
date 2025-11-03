from fastapi import APIRouter, HTTPException, status, Depends
from datetime import datetime
from bson import ObjectId
from typing import List, Optional

from ..models import MealCreate, MealUpdate, MealResponse, MealStatus
from app.database import get_database
from app.dependencies import get_current_user

router = APIRouter(prefix="/api/meals", tags=["Meals"])


# Helper function to serialize MongoDB meal
def meal_to_response(meal: dict, seller: dict) -> MealResponse:
    """Convert MongoDB meal document to MealResponse"""
    return MealResponse(
        id=str(meal["_id"]),
        seller_id=str(meal["seller_id"]),
        seller_name=seller["full_name"],
        seller_rating=seller.get("stats", {}).get("average_rating", 0.0),
        title=meal["title"],
        description=meal["description"],
        cuisine_type=meal["cuisine_type"],
        meal_type=meal["meal_type"],
        photos=meal.get("photos", []),
        allergen_info=meal["allergen_info"],
        nutrition_info=meal.get("nutrition_info"),
        portion_size=meal["portion_size"],
        available_for_sale=meal["available_for_sale"],
        sale_price=meal.get("sale_price"),
        available_for_swap=meal["available_for_swap"],
        swap_preferences=meal.get("swap_preferences", []),
        status=meal["status"],
        preparation_date=meal["preparation_date"],
        expires_date=meal["expires_date"],
        pickup_instructions=meal.get("pickup_instructions"),
        average_rating=meal.get("average_rating", 0.0),
        total_reviews=meal.get("total_reviews", 0),
        views=meal.get("views", 0),
        created_at=meal["created_at"],
        updated_at=meal["updated_at"],
    )


# Create a new meal
@router.post("/", response_model=MealResponse, status_code=status.HTTP_201_CREATED)
async def create_meal(meal: MealCreate, current_user: dict = Depends(get_current_user)):
    """Create a new meal listing"""
    db = get_database()

    meal_doc = {
        "seller_id": current_user["_id"],
        "title": meal.title,
        "description": meal.description,
        "cuisine_type": meal.cuisine_type,
        "meal_type": meal.meal_type,
        "photos": meal.photos,
        "allergen_info": meal.allergen_info.model_dump(),
        "nutrition_info": (
            meal.nutrition_info.model_dump() if meal.nutrition_info else None
        ),
        "portion_size": meal.portion_size,
        "available_for_sale": meal.available_for_sale,
        "sale_price": meal.sale_price,
        "available_for_swap": meal.available_for_swap,
        "swap_preferences": meal.swap_preferences,
        "status": MealStatus.AVAILABLE,
        "preparation_date": meal.preparation_date,
        "expires_date": meal.expires_date,
        "pickup_instructions": meal.pickup_instructions,
        "average_rating": 0.0,
        "total_reviews": 0,
        "views": 0,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
    }

    result = await db.meals.insert_one(meal_doc)

    # Fetch the created meal
    created_meal = await db.meals.find_one({"_id": result.inserted_id})

    return meal_to_response(created_meal, current_user)


# Get all meals with filters
@router.get("/", response_model=List[MealResponse])
async def get_meals(
    cuisine_type: Optional[str] = None,
    meal_type: Optional[str] = None,
    max_price: Optional[float] = None,
    available_for_sale: Optional[bool] = None,
    available_for_swap: Optional[bool] = None,
    skip: int = 0,
    limit: int = 20,
):
    """Get all available meals with optional filters"""
    db = get_database()

    # Build query filters
    query = {"status": MealStatus.AVAILABLE}

    if cuisine_type:
        query["cuisine_type"] = cuisine_type
    if meal_type:
        query["meal_type"] = meal_type
    if max_price is not None:
        query["sale_price"] = {"$lte": max_price}
    if available_for_sale is not None:
        query["available_for_sale"] = available_for_sale
    if available_for_swap is not None:
        query["available_for_swap"] = available_for_swap

    # Fetch meals
    meals_cursor = db.meals.find(query).skip(skip).limit(limit).sort("created_at", -1)
    meals = await meals_cursor.to_list(length=limit)

    # Fetch sellers for each meal
    meal_responses = []
    for meal in meals:
        seller = await db.users.find_one({"_id": meal["seller_id"]})
        if seller:
            meal_responses.append(meal_to_response(meal, seller))

    return meal_responses


# Get meal by ID
@router.get("/{meal_id}", response_model=MealResponse)
async def get_meal_by_id(meal_id: str):
    """Get a specific meal by ID"""
    db = get_database()

    if not ObjectId.is_valid(meal_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid meal ID"
        )

    meal = await db.meals.find_one({"_id": ObjectId(meal_id)})
    if not meal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Meal not found"
        )

    # Increment views
    await db.meals.update_one({"_id": ObjectId(meal_id)}, {"$inc": {"views": 1}})
    meal["views"] = meal.get("views", 0) + 1

    # Fetch seller
    seller = await db.users.find_one({"_id": meal["seller_id"]})
    if not seller:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Seller not found"
        )

    return meal_to_response(meal, seller)


# Get my meals
@router.get("/my/listings", response_model=List[MealResponse])
async def get_my_meals(current_user: dict = Depends(get_current_user)):
    """Get all meals created by the authenticated user"""
    db = get_database()

    meals_cursor = db.meals.find({"seller_id": current_user["_id"]}).sort(
        "created_at", -1
    )
    meals = await meals_cursor.to_list(length=100)

    meal_responses = [meal_to_response(meal, current_user) for meal in meals]
    return meal_responses


# Update a meal
@router.put("/{meal_id}", response_model=MealResponse)
async def update_meal(
    meal_id: str,
    meal_update: MealUpdate,
    current_user: dict = Depends(get_current_user),
):
    """Update a meal listing"""
    db = get_database()

    if not ObjectId.is_valid(meal_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid meal ID"
        )

    # Check if meal exists and belongs to user
    meal = await db.meals.find_one({"_id": ObjectId(meal_id)})
    if not meal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Meal not found"
        )

    if meal["seller_id"] != current_user["_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to update this meal",
        )

    # Build update document
    update_data = {"updated_at": datetime.utcnow()}

    if meal_update.title is not None:
        update_data["title"] = meal_update.title
    if meal_update.description is not None:
        update_data["description"] = meal_update.description
    if meal_update.cuisine_type is not None:
        update_data["cuisine_type"] = meal_update.cuisine_type
    if meal_update.meal_type is not None:
        update_data["meal_type"] = meal_update.meal_type
    if meal_update.photos is not None:
        update_data["photos"] = meal_update.photos
    if meal_update.allergen_info is not None:
        update_data["allergen_info"] = meal_update.allergen_info.model_dump()
    if meal_update.nutrition_info is not None:
        update_data["nutrition_info"] = meal_update.nutrition_info.model_dump()
    if meal_update.portion_size is not None:
        update_data["portion_size"] = meal_update.portion_size
    if meal_update.available_for_sale is not None:
        update_data["available_for_sale"] = meal_update.available_for_sale
    if meal_update.sale_price is not None:
        update_data["sale_price"] = meal_update.sale_price
    if meal_update.available_for_swap is not None:
        update_data["available_for_swap"] = meal_update.available_for_swap
    if meal_update.swap_preferences is not None:
        update_data["swap_preferences"] = meal_update.swap_preferences
    if meal_update.status is not None:
        update_data["status"] = meal_update.status
    if meal_update.pickup_instructions is not None:
        update_data["pickup_instructions"] = meal_update.pickup_instructions

    # Update meal
    result = await db.meals.update_one(
        {"_id": ObjectId(meal_id)}, {"$set": update_data}
    )

    if result.modified_count == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="No changes made to meal"
        )

    # Fetch updated meal
    updated_meal = await db.meals.find_one({"_id": ObjectId(meal_id)})
    return meal_to_response(updated_meal, current_user)


# Delete a meal
@router.delete("/{meal_id}")
async def delete_meal(meal_id: str, current_user: dict = Depends(get_current_user)):
    """Delete a meal listing"""
    db = get_database()

    if not ObjectId.is_valid(meal_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid meal ID"
        )

    # Check if meal exists and belongs to user
    meal = await db.meals.find_one({"_id": ObjectId(meal_id)})
    if not meal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Meal not found"
        )

    if meal["seller_id"] != current_user["_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to delete this meal",
        )

    # Delete meal
    result = await db.meals.delete_one({"_id": ObjectId(meal_id)})

    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Meal not found"
        )

    return {"message": "Meal successfully deleted"}
