from fastapi import APIRouter, HTTPException, status
from typing import List
from bson import ObjectId
from ..models import ItemModel, ItemCreate, ItemUpdate
from ..database import get_database

router = APIRouter(prefix="/items", tags=["items"])

@router.get("/", response_model=List[ItemModel])
async def get_items():
    db = get_database()
    items = []
    async for item in db.items.find():
        items.append(ItemModel(**item))
    return items

@router.get("/{item_id}", response_model=ItemModel)
async def get_item(item_id: str):
    if not ObjectId.is_valid(item_id):
        raise HTTPException(status_code=400, detail="Invalid item ID")
    
    db = get_database()
    item = await db.items.find_one({"_id": ObjectId(item_id)})
    
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    
    return ItemModel(**item)

@router.post("/", response_model=ItemModel, status_code=status.HTTP_201_CREATED)
async def create_item(item: ItemCreate):
    db = get_database()
    item_dict = item.model_dump()
    result = await db.items.insert_one(item_dict)
    created_item = await db.items.find_one({"_id": result.inserted_id})
    return ItemModel(**created_item)

@router.put("/{item_id}", response_model=ItemModel)
async def update_item(item_id: str, item: ItemUpdate):
    if not ObjectId.is_valid(item_id):
        raise HTTPException(status_code=400, detail="Invalid item ID")
    
    db = get_database()
    update_data = {k: v for k, v in item.model_dump().items() if v is not None}
    
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")
    
    result = await db.items.update_one(
        {"_id": ObjectId(item_id)},
        {"$set": update_data}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    
    updated_item = await db.items.find_one({"_id": ObjectId(item_id)})
    return ItemModel(**updated_item)

@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: str):
    if not ObjectId.is_valid(item_id):
        raise HTTPException(status_code=400, detail="Invalid item ID")
    
    db = get_database()
    result = await db.items.delete_one({"_id": ObjectId(item_id)})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    
    return None