# Taste Buddies API Documentation

**Version:** 1.0.0  
**Description:** A full-stack application connecting neighbors through homemade meals

---

## Table of Contents

1. [Overview](#overview)
2. [Deployment Guide](#deployment-guide)
3. [API Reference](#api-reference)
4. [Troubleshooting](#troubleshooting)
5. [Development Guide](#development-guide)

---

## Overview

Taste Buddies is a neighborhood meal-sharing platform that allows users to:
- List homemade meals for sale or swap
- Discover meals from local home cooks
- Build community through food sharing
- Review and rate meals

**Technology Stack:**
- **Backend:** FastAPI (Python)
- **Database:** MongoDB
- **Frontend:** React (port 5173)
- **Containerization:** Docker & Docker Compose

---

## Deployment Guide

### Prerequisites

Before deploying Taste Buddies, ensure you have:

1. **Git** (version 2.0+)
   - Download: https://git-scm.com/downloads
   - Verify: `git --version`

2. **Docker** (version 20.0+)
   - Download: https://docs.docker.com/get-docker/
   - Verify: `docker --version`

3. **Docker Compose** (version 2.0+)
   - Included with Docker Desktop
   - Verify: `docker-compose --version`

4. **Docker Desktop** (recommended for container management)
   - Download: https://www.docker.com/products/docker-desktop

### Step-by-Step Deployment

#### 1. Clone the Repository

```bash
# Navigate to your desired directory
cd /path/to/your/workspace

# Clone the repository
git clone https://github.com/madisonbook/CSC510.git

# Navigate into the project
cd CSC510
```

#### 2. Navigate to Project Directory

```bash
cd proj2
```

#### 3. Configure Environment Variables (Optional)

Create a `.env` file in the `proj2` directory if you need custom configuration:

```env
MONGODB_URL=mongodb://mongodb:27017
DATABASE_NAME=tastebuddies
```

#### 4. Build and Start the Application

```bash
# Build and start all services
docker-compose up --build
```

**What happens:**
- MongoDB container starts on port 27017
- Backend API starts on port 8000
- Frontend starts on port 5173
- Database indexes are automatically created

#### 5. Access the Application

Open your browser and navigate to:
- **Frontend:** http://localhost:5173
- **API Documentation:** http://localhost:8000/docs
- **Health Check:** http://localhost:8000/health

#### 6. Verify Installation

Check that all services are running:
```bash
docker-compose ps
```

You should see three services running:
- `mongodb`
- `backend`
- `frontend`

### Stopping the Application

```bash
# Stop services (keeps data)
docker-compose down

# OR press Ctrl+C in the terminal running docker-compose
```

### Complete Cleanup

```bash
# Stop services and remove volumes (deletes all data)
docker-compose down -v
```

### Running in Background (Detached Mode)

```bash
# Start services in background
docker-compose up -d --build

# View logs
docker-compose logs -f

# Stop background services
docker-compose down
```

### Running Backend Tests

```bash
# Run the test suite
docker-compose up --build backend-tests
```

---

## API Reference

### Base URL

```
http://localhost:8000
```

### Authentication

Most endpoints require authentication using Bearer tokens. Include the token in the Authorization header:

```
Authorization: Bearer <your-token>
```

**Note:** Current implementation uses email as token (temporary). Production should use JWT.

---

### Authentication Endpoints

#### Register User

**POST** `/api/auth/register/user`

Creates a new user account and sends verification email.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "SecurePass123",
  "full_name": "John Doe",
  "phone": "+1234567890",
  "location": {
    "address": "123 Main St",
    "city": "Raleigh",
    "state": "NC",
    "zip_code": "27601",
    "latitude": 35.7796,
    "longitude": -78.6382
  },
  "bio": "Love cooking Italian food!",
  "profile_picture": "https://example.com/photo.jpg"
}
```

**Password Requirements:**
- Minimum 8 characters
- Maximum 72 characters
- At least one uppercase letter
- At least one lowercase letter
- At least one number

**Response:** `201 Created`
```json
{
  "message": "User account created successfully. Please check your email to verify your account.",
  "user_id": "507f1f77bcf86cd799439011",
  "email": "user@example.com"
}
```

**Error Responses:**
- `400 Bad Request` - Email already exists or invalid data
- `422 Unprocessable Entity` - Validation errors

#### Verify Email

**GET** `/api/auth/verify`

Verifies user email address using token from verification email.

**Query Parameters:**
- `email` (string, required) - User's email address
- `token` (string, required) - Verification token from email

**Response:** `200 OK`
```json
{
  "message": "Email verified successfully!",
  "verified": true
}
```

**Error Responses:**
- `400 Bad Request` - Invalid or expired token

#### Login

**POST** `/api/auth/login`

Authenticates user and returns user information.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "SecurePass123"
}
```

**Response:** `200 OK`
```json
{
  "message": "Login successful",
  "user_id": "507f1f77bcf86cd799439011",
  "email": "user@example.com",
  "role": "user",
  "full_name": "John Doe"
}
```

**Error Responses:**
- `401 Unauthorized` - Incorrect credentials
- `403 Forbidden` - Email not verified

#### Resend Verification Email

**POST** `/api/auth/resend-verification`

Sends a new verification email.

**Query Parameters:**
- `email` (string, required) - User's email address
- `account_type` (string, optional) - Default: "user"

**Response:** `200 OK`
```json
{
  "message": "Verification email sent successfully"
}
```

---

### User Endpoints

#### Get Current User Profile

**GET** `/api/users/me`

Returns authenticated user's complete profile.

**Headers:**
```
Authorization: Bearer <token>
```

**Response:** `200 OK`
```json
{
  "id": "507f1f77bcf86cd799439011",
  "email": "user@example.com",
  "full_name": "John Doe",
  "phone": "+1234567890",
  "location": {
    "address": "123 Main St",
    "city": "Raleigh",
    "state": "NC",
    "zip_code": "27601",
    "latitude": 35.7796,
    "longitude": -78.6382
  },
  "bio": "Love cooking Italian food!",
  "profile_picture": "https://example.com/photo.jpg",
  "dietary_preferences": {
    "dietary_restrictions": ["vegetarian"],
    "allergens": ["peanuts"],
    "cuisine_preferences": ["Italian", "Mexican"],
    "spice_level": "medium"
  },
  "social_media": {
    "facebook": "https://facebook.com/johndoe",
    "instagram": "@johndoe",
    "twitter": "@johndoe"
  },
  "role": "user",
  "status": "active",
  "stats": {
    "total_meals_sold": 10,
    "total_meals_swapped": 5,
    "total_meals_purchased": 8,
    "average_rating": 4.5,
    "total_reviews": 12,
    "badges": []
  },
  "created_at": "2024-01-15T10:30:00",
  "verified": true
}
```

#### Get User by ID

**GET** `/api/users/{user_id}`

Returns public profile of any user.

**Path Parameters:**
- `user_id` (string, required) - MongoDB ObjectId

**Response:** `200 OK` - Same structure as Get Current User Profile

**Error Responses:**
- `400 Bad Request` - Invalid user ID format
- `404 Not Found` - User not found

#### Update User Profile

**PUT** `/api/users/me`

Updates authenticated user's profile information.

**Headers:**
```
Authorization: Bearer <token>
```

**Request Body** (all fields optional):
```json
{
  "full_name": "Jane Doe",
  "phone": "+1234567890",
  "location": {
    "address": "456 Oak Ave",
    "city": "Durham",
    "state": "NC",
    "zip_code": "27701"
  },
  "bio": "Passionate about healthy cooking",
  "profile_picture": "https://example.com/new-photo.jpg"
}
```

**Response:** `200 OK` - Updated user profile

**Error Responses:**
- `400 Bad Request` - No changes made or invalid data
- `401 Unauthorized` - Not authenticated

#### Update Dietary Preferences

**PUT** `/api/users/me/dietary-preferences`

Updates user's dietary preferences and restrictions.

**Request Body:**
```json
{
  "dietary_restrictions": ["vegetarian", "gluten-free"],
  "allergens": ["peanuts", "shellfish"],
  "cuisine_preferences": ["Italian", "Thai", "Mediterranean"],
  "spice_level": "hot"
}
```

**Response:** `200 OK` - Updated user profile

#### Update Social Media Links

**PUT** `/api/users/me/social-media`

Updates user's social media links for identity verification.

**Request Body:**
```json
{
  "facebook": "https://facebook.com/johndoe",
  "instagram": "@johndoe_chef",
  "twitter": "@johndoe"
}
```

**Response:** `200 OK` - Updated user profile

#### Delete User Account

**DELETE** `/api/users/me`

Permanently deletes user account and all associated data.

**Headers:**
```
Authorization: Bearer <token>
```

**Response:** `200 OK`
```json
{
  "message": "Account successfully deleted"
}
```

**What gets deleted:**
- User account
- All meal listings
- All reviews written by user

#### Get User Statistics

**GET** `/api/users/me/stats`

Returns authenticated user's statistics and badges.

**Response:** `200 OK`
```json
{
  "total_meals_sold": 10,
  "total_meals_swapped": 5,
  "total_meals_purchased": 8,
  "average_rating": 4.5,
  "total_reviews": 12,
  "badges": [
    {
      "badge_type": "verified_seller",
      "earned_date": "2024-02-01T10:00:00",
      "description": "Completed email verification"
    }
  ]
}
```

---

### Meal Endpoints

#### Create Meal

**POST** `/api/meals/`

Creates a new meal listing.

**Headers:**
```
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "title": "Homemade Lasagna",
  "description": "Traditional Italian lasagna with homemade pasta, beef ragu, and bechamel sauce",
  "cuisine_type": "Italian",
  "meal_type": "dinner",
  "photos": [
    "https://example.com/lasagna1.jpg",
    "https://example.com/lasagna2.jpg"
  ],
  "allergen_info": {
    "contains": ["dairy", "eggs", "gluten"],
    "may_contain": ["nuts"]
  },
  "nutrition_info": {
    "calories": 450,
    "protein_grams": 25.5,
    "carbs_grams": 40.0,
    "fat_grams": 18.5
  },
  "portion_size": "Serves 4",
  "available_for_sale": true,
  "sale_price": 25.00,
  "available_for_swap": true,
  "swap_preferences": ["Thai curry", "Mexican enchiladas"],
  "preparation_date": "2024-10-22T14:00:00",
  "expires_date": "2024-10-24T20:00:00",
  "pickup_instructions": "Pick up from side door between 5-7 PM"
}
```

**Field Validation:**
- `title`: 3-100 characters
- `description`: 10-1000 characters
- `sale_price`: Must be > 0 if available_for_sale is true
- `preparation_date`: Past or present date
- `expires_date`: Must be after preparation_date

**Response:** `201 Created`
```json
{
  "id": "507f1f77bcf86cd799439011",
  "seller_id": "507f1f77bcf86cd799439012",
  "seller_name": "John Doe",
  "seller_rating": 4.5,
  "title": "Homemade Lasagna",
  "description": "Traditional Italian lasagna...",
  "cuisine_type": "Italian",
  "meal_type": "dinner",
  "photos": ["https://example.com/lasagna1.jpg"],
  "allergen_info": {
    "contains": ["dairy", "eggs", "gluten"],
    "may_contain": ["nuts"]
  },
  "nutrition_info": {
    "calories": 450,
    "protein_grams": 25.5,
    "carbs_grams": 40.0,
    "fat_grams": 18.5
  },
  "portion_size": "Serves 4",
  "available_for_sale": true,
  "sale_price": 25.00,
  "available_for_swap": true,
  "swap_preferences": ["Thai curry", "Mexican enchiladas"],
  "status": "available",
  "preparation_date": "2024-10-22T14:00:00",
  "expires_date": "2024-10-24T20:00:00",
  "pickup_instructions": "Pick up from side door between 5-7 PM",
  "average_rating": 0.0,
  "total_reviews": 0,
  "views": 0,
  "created_at": "2024-10-22T10:00:00",
  "updated_at": "2024-10-22T10:00:00"
}
```

#### Get All Meals

**GET** `/api/meals/`

Returns paginated list of available meals with optional filters.

**Query Parameters:**
- `cuisine_type` (string, optional) - Filter by cuisine
- `meal_type` (string, optional) - Filter by meal type
- `max_price` (float, optional) - Maximum price
- `available_for_sale` (boolean, optional) - Filter by sale availability
- `available_for_swap` (boolean, optional) - Filter by swap availability
- `skip` (integer, optional) - Number of records to skip (default: 0)
- `limit` (integer, optional) - Maximum records to return (default: 20)

**Example Request:**
```
GET /api/meals/?cuisine_type=Italian&max_price=30.00&skip=0&limit=10
```

**Response:** `200 OK`
```json
[
  {
    "id": "507f1f77bcf86cd799439011",
    "seller_id": "507f1f77bcf86cd799439012",
    "seller_name": "John Doe",
    "seller_rating": 4.5,
    ...
  }
]
```

#### Get Meal by ID

**GET** `/api/meals/{meal_id}`

Returns detailed information about a specific meal. Automatically increments view count.

**Path Parameters:**
- `meal_id` (string, required) - MongoDB ObjectId

**Response:** `200 OK` - Single meal object

**Error Responses:**
- `400 Bad Request` - Invalid meal ID format
- `404 Not Found` - Meal not found

#### Get My Meals

**GET** `/api/meals/my/listings`

Returns all meals created by authenticated user.

**Headers:**
```
Authorization: Bearer <token>
```

**Response:** `200 OK` - Array of meal objects sorted by creation date (newest first)

#### Update Meal

**PUT** `/api/meals/{meal_id}`

Updates an existing meal listing. Only the meal owner can update.

**Headers:**
```
Authorization: Bearer <token>
```

**Path Parameters:**
- `meal_id` (string, required) - MongoDB ObjectId

**Request Body** (all fields optional):
```json
{
  "title": "Updated Lasagna Recipe",
  "sale_price": 28.00,
  "status": "sold",
  "pickup_instructions": "New pickup location"
}
```

**Available Status Values:**
- `available` - Meal is available
- `pending` - Transaction in progress
- `sold` - Meal has been sold
- `swapped` - Meal has been swapped
- `unavailable` - Temporarily unavailable

**Response:** `200 OK` - Updated meal object

**Error Responses:**
- `400 Bad Request` - Invalid meal ID or no changes made
- `403 Forbidden` - Not the meal owner
- `404 Not Found` - Meal not found

#### Delete Meal

**DELETE** `/api/meals/{meal_id}`

Permanently deletes a meal listing. Only the meal owner can delete.

**Headers:**
```
Authorization: Bearer <token>
```

**Path Parameters:**
- `meal_id` (string, required) - MongoDB ObjectId

**Response:** `200 OK`
```json
{
  "message": "Meal successfully deleted"
}
```

**Error Responses:**
- `400 Bad Request` - Invalid meal ID
- `403 Forbidden` - Not the meal owner
- `404 Not Found` - Meal not found

---

### System Endpoints

#### Root

**GET** `/`

Returns API welcome message.

**Response:** `200 OK`
```json
{
  "message": "Welcome to Taste Buddiez API",
  "tagline": "Connecting neighbors through homemade meals"
}
```

#### Health Check

**GET** `/health`

Returns API health status.

**Response:** `200 OK`
```json
{
  "status": "healthy"
}
```

#### Debug: List Users

**GET** `/api/debug/users`

Returns list of all users (development only, limit 100).

**Response:** `200 OK` - Array of user objects

---

## Troubleshooting

### Common Issues and Solutions

#### Issue: Port Already in Use

**Symptoms:**
```
Error: Bind for 0.0.0.0:5173 failed: port is already allocated
```

**Solution:**
1. Check what's using the port:
   ```bash
   # On Linux/Mac
   lsof -i :5173
   
   # On Windows
   netstat -ano | findstr :5173
   ```

2. Stop the conflicting process or change the port in `docker-compose.yml`

3. Restart Docker services:
   ```bash
   docker-compose down
   docker-compose up --build
   ```

---

#### Issue: MongoDB Connection Failed

**Symptoms:**
```
pymongo.errors.ServerSelectionTimeoutError: localhost:27017: [Errno 111] Connection refused
```

**Solution:**
1. Ensure MongoDB container is running:
   ```bash
   docker-compose ps
   ```

2. Check MongoDB logs:
   ```bash
   docker-compose logs mongodb
   ```

3. Restart MongoDB:
   ```bash
   docker-compose restart mongodb
   ```

4. If persistent, remove volumes and rebuild:
   ```bash
   docker-compose down -v
   docker-compose up --build
   ```

---

#### Issue: Database Indexes Not Created

**Symptoms:**
```
⚠️ Index creation note: E11000 duplicate key error
```

**Solution:**
This warning is usually harmless (indexes already exist). If you need to rebuild indexes:

1. Stop the application:
   ```bash
   docker-compose down
   ```

2. Remove database volumes:
   ```bash
   docker-compose down -v
   ```

3. Restart and rebuild:
   ```bash
   docker-compose up --build
   ```

---

#### Issue: Authentication Failed (401 Unauthorized)

**Symptoms:**
```json
{
  "detail": "Not authenticated"
}
```

**Solution:**
1. Ensure you're including the Authorization header:
   ```
   Authorization: Bearer <your-email>
   ```

2. Verify your email is verified:
   - Check verification email
   - Use the verification link

3. Test with debug endpoint:
   ```bash
   curl http://localhost:8000/api/debug/users
   ```

---

#### Issue: Email Verification Not Working

**Symptoms:**
- No verification email received
- Verification link returns error

**Solution:**
1. Check if verification email functionality is configured (currently mock implementation)

2. Manually verify user in database:
   ```bash
   docker exec -it <mongodb-container> mongosh
   use tastebuddies
   db.users.updateOne(
     {email: "user@example.com"},
     {$set: {verified: true, status: "active"}}
   )
   ```

3. Find container name:
   ```bash
   docker-compose ps
   ```

---

#### Issue: Docker Build Fails

**Symptoms:**
```
ERROR [backend internal] load metadata for docker.io/library/python:3.11-slim
```

**Solution:**
1. Check Docker daemon is running:
   ```bash
   docker info
   ```

2. Check internet connection

3. Clear Docker cache:
   ```bash
   docker system prune -a
   ```

4. Rebuild:
   ```bash
   docker-compose build --no-cache
   docker-compose up
   ```

---

#### Issue: Frontend Not Loading

**Symptoms:**
- Browser shows "Can't reach this page"
- `http://localhost:5173` doesn't load

**Solution:**
1. Check frontend container status:
   ```bash
   docker-compose ps
   ```

2. View frontend logs:
   ```bash
   docker-compose logs frontend
   ```

3. Restart frontend service:
   ```bash
   docker-compose restart frontend
   ```

4. Access frontend inside container:
   ```bash
   docker-compose exec frontend sh
   ```

---

#### Issue: Backend Tests Failing

**Symptoms:**
```
FAILED tests/test_auth.py::test_register_user
```

**Solution:**
1. Check test logs:
   ```bash
   docker-compose logs backend-tests
   ```

2. Ensure test database is clean:
   ```bash
   docker-compose down -v
   docker-compose up backend-tests --build
   ```

3. Run tests with verbose output:
   ```bash
   docker-compose run backend-tests pytest -v
   ```

---

#### Issue: Password Validation Errors

**Symptoms:**
```json
{
  "detail": [
    {
      "msg": "Password must contain at least one uppercase letter"
    }
  ]
}
```

**Solution:**
Ensure password meets all requirements:
- ✓ At least 8 characters
- ✓ Maximum 72 characters
- ✓ At least one uppercase letter (A-Z)
- ✓ At least one lowercase letter (a-z)
- ✓ At least one number (0-9)

Example valid password: `MyPass123`

---

#### Issue: Invalid ObjectId Format

**Symptoms:**
```json
{
  "detail": "Invalid meal ID"
}
```

**Solution:**
1. Ensure you're using valid MongoDB ObjectId format (24 hex characters)

2. Example valid ObjectId: `507f1f77bcf86cd799439011`

3. Get valid IDs from API responses or database queries

---

### Error Response Reference

All API errors follow this format:

```json
{
  "detail": "Error message description"
}
```

**HTTP Status Codes:**
- `400 Bad Request` - Invalid input data
- `401 Unauthorized` - Authentication required or failed
- `403 Forbidden` - Insufficient permissions
- `404 Not Found` - Resource not found
- `422 Unprocessable Entity` - Validation errors
- `500 Internal Server Error` - Server error

---

### Getting Help

If you encounter issues not covered here:

1. **Check Logs:**
   ```bash
   docker-compose logs -f
   ```

2. **View Specific Service Logs:**
   ```bash
   docker-compose logs backend
   docker-compose logs frontend
   docker-compose logs mongodb
   ```

3. **Check API Documentation:**
   Visit http://localhost:8000/docs for interactive API docs

4. **Verify Service Health:**
   ```bash
   curl http://localhost:8000/health
   ```

5. **Report Issues:**
   - GitHub: https://github.com/madisonbook/CSC510/issues
   - Include: Error messages, logs, and steps to reproduce

---

## Development Guide

### Project Structure

```
proj2/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── models.py            # Pydantic models and schemas
│   ├── database.py          # MongoDB connection management
│   ├── dependencies.py      # Authentication dependencies
│   ├── utils.py            # Utility functions (hashing, tokens)
│   └── routes/
│       ├── auth_routes.py   # Authentication endpoints
│       ├── user_routes.py   # User management endpoints
│       └── meal_routes.py   # Meal management endpoints
├── tests/                   # Test files
├── Dockerfile              # Backend container configuration
├── docker-compose.yml      # Multi-container orchestration
└── requirements.txt        # Python dependencies
```

### Local Development Setup

#### Without Docker

1. **Install Python 3.11+**

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Start MongoDB:**
   ```bash
   # Using Docker
   docker run -d -p 27017:27017 --name mongodb mongo:latest
   
   # Or install MongoDB locally
   ```

4. **Set environment variables:**
   ```bash
   export MONGODB_URL=mongodb://localhost:27017
   export DATABASE_NAME=tastebuddies
   ```

5. **Run the application:**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

#### Running Tests Locally

```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx pytest-cov

# Run tests
pytest

# Run with coverage
pytest --cov=app tests/

# Run specific test file
pytest tests/test_auth.py -v
```

### Code Quality

#### Linting

```bash
# Install flake8
pip install flake8

# Run linter
flake8 app/

# Run with specific rules
flake8 app/ --max-line-length=100
```

#### Code Coverage

View coverage report after running tests:
```bash
pytest --cov=app --cov-report=html tests/
# Open htmlcov/index.html in browser
```

### Database Management

#### Accessing MongoDB Shell

```bash
# Enter MongoDB container
docker exec -it <mongodb-container-name> mongosh

# Use database
use tastebuddies

# View collections
show collections

# Query users
db.users.find().pretty()

# Query meals
db.meals.find({status: "available"}).pretty()
```

#### Database Indexes

Indexes are automatically created on startup:

**Users Collection:**
- `email` (unique)

**Meals Collection:**
- `seller_id`
- `status`
- `cuisine_type`
- `created_at`

**Reviews Collection:**
- `meal_id`
- `reviewer_id`
- `seller_id`

**Verification Tokens Collection:**
- `expires_at` (TTL index)
- `email`

### Adding New Endpoints

1. **Define Pydantic models** in `models.py`
2. **Create route handler** in appropriate route file
3. **Add authentication** if needed using `Depends(get_current_user)`
4. **Write tests** for the endpoint
5. **Update this documentation**

Example:
```python
from fastapi import APIRouter, Depends
from app.dependencies import get_current_user

router = APIRouter(prefix="/api/example", tags=["Example"])

@router.get("/")
async def get_example(current_user: dict = Depends(get_current_user)):
    return {"message": "Hello, authenticated user!"}
```

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `MONGODB_URL` | `mongodb://mongodb:27017` | MongoDB connection string |
| `DATABASE_NAME` | `myapp` | Database name |

### Docker Commands Reference

```bash
# Build without cache
docker-compose build --no-cache

# View container resource usage
docker stats

# Execute command in container
docker-compose exec backend bash

# View container details
docker inspect <container-name>

# Remove all stopped containers
docker-compose rm

# Scale a service (if applicable)
docker-compose up --scale backend=3
```

---

## API Libraries & SDKs

### Python Client Example

```python
import requests

BASE_URL = "http://localhost:8000"

# Register user
response = requests.post(f"{BASE_URL}/api/auth/register/user", json={
    "email": "user@example.com",
    "password": "SecurePass123",
    "full_name": "John Doe",
    "location": {
        "address": "123 Main St",
        "city": "Raleigh",
        "state": "NC",
        "zip_code": "27601"
    }
})
print(response.json())

# Login
response = requests.post(f"{BASE_URL}/api/auth/login", json={
    "email": "user@example.com",
    "password": "SecurePass123"
})
user_data = response.json()

# Use token for authenticated requests
headers = {"Authorization": f"Bearer {user_data['email']}"}

# Get current user profile
response = requests.get(f"{BASE_URL}/api/users/me", headers=headers)
print(response.json())

# Create meal
response = requests.post(f"{BASE_URL}/api/meals/", headers=headers, json={
    "title": "Homemade Pizza",
    "description": "Delicious wood-fired pizza",
    "cuisine_type": "Italian",
    "meal_type": "dinner",
    "photos": [],
    "allergen_info": {"contains": ["gluten", "dairy"], "may_contain": []},
    "portion_size": "Serves 2",
    "available_for_sale": True,
    "sale_price": 15.00,
    "available_for_swap": False,
    "swap_preferences": [],
    "preparation_date": "2024-10-22T18:00:00",
    "expires_date": "2024-10-23T20:00:00"
})
print(response.json())
```

### JavaScript/Node.js Client Example

```javascript
const axios = require('axios');

const BASE_URL = 'http://localhost:8000';

// Register user
async function registerUser() {
  try {
    const response = await axios.post(`${BASE_URL}/api/auth/register/user`, {
      email: 'user@example.com',
      password: 'SecurePass123',
      full_name: 'John Doe',
      location: {
        address: '123 Main St',
        city: 'Raleigh',
        state: 'NC',
        zip_code: '27601'
      }
    });
    console.log(response.data);
    return response.data;
  } catch (error) {
    console.error('Registration failed:', error.response.data);
  }
}

// Login
async function login(email, password) {
  try {
    const response = await axios.post(`${BASE_URL}/api/auth/login`, {
      email,
      password
    });
    return response.data;
  } catch (error) {
    console.error('Login failed:', error.response.data);
  }
}

// Get meals with authentication
async function getMeals(token) {
  try {
    const response = await axios.get(`${BASE_URL}/api/meals/`, {
      headers: {
        'Authorization': `Bearer ${token}`
      },
      params: {
        cuisine_type: 'Italian',
        max_price: 30.00,
        limit: 10
      }
    });
    return response.data;
  } catch (error) {
    console.error('Failed to fetch meals:', error.response.data);
  }
}

// Create meal
async function createMeal(token, mealData) {
  try {
    const response = await axios.post(`${BASE_URL}/api/meals/`, mealData, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });
    return response.data;
  } catch (error) {
    console.error('Failed to create meal:', error.response.data);
  }
}

// Usage
(async () => {
  await registerUser();
  const loginData = await login('user@example.com', 'SecurePass123');
  const meals = await getMeals(loginData.email);
  console.log('Available meals:', meals);
})();
```

### cURL Examples

#### Register User
```bash
curl -X POST "http://localhost:8000/api/auth/register/user" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePass123",
    "full_name": "John Doe",
    "location": {
      "address": "123 Main St",
      "city": "Raleigh",
      "state": "NC",
      "zip_code": "27601"
    }
  }'
```

#### Login
```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePass123"
  }'
```

#### Get User Profile
```bash
curl -X GET "http://localhost:8000/api/users/me" \
  -H "Authorization: Bearer user@example.com"
```

#### Create Meal
```bash
curl -X POST "http://localhost:8000/api/meals/" \
  -H "Authorization: Bearer user@example.com" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Homemade Lasagna",
    "description": "Traditional Italian lasagna with fresh ingredients",
    "cuisine_type": "Italian",
    "meal_type": "dinner",
    "photos": [],
    "allergen_info": {
      "contains": ["dairy", "gluten"],
      "may_contain": []
    },
    "portion_size": "Serves 4",
    "available_for_sale": true,
    "sale_price": 25.00,
    "available_for_swap": false,
    "swap_preferences": [],
    "preparation_date": "2024-10-22T14:00:00",
    "expires_date": "2024-10-24T20:00:00"
  }'
```

#### Get All Meals with Filters
```bash
curl -X GET "http://localhost:8000/api/meals/?cuisine_type=Italian&max_price=30&limit=10"
```

#### Update Meal
```bash
curl -X PUT "http://localhost:8000/api/meals/507f1f77bcf86cd799439011" \
  -H "Authorization: Bearer user@example.com" \
  -H "Content-Type: application/json" \
  -d '{
    "sale_price": 28.00,
    "status": "sold"
  }'
```

#### Delete Meal
```bash
curl -X DELETE "http://localhost:8000/api/meals/507f1f77bcf86cd799439011" \
  -H "Authorization: Bearer user@example.com"
```

---

## Data Models Reference

### User Data Model

```python
{
  "_id": ObjectId,                    # MongoDB document ID
  "email": str,                       # Unique email address
  "password": str,                    # Hashed password (bcrypt)
  "full_name": str,                   # User's full name
  "phone": str | None,                # Phone number (optional)
  "location": {
    "address": str,                   # Street address
    "city": str,                      # City name
    "state": str,                     # State/province
    "zip_code": str,                  # Postal code
    "latitude": float | None,         # GPS coordinates (optional)
    "longitude": float | None
  },
  "bio": str | None,                  # User biography
  "profile_picture": str | None,      # Profile picture URL
  "dietary_preferences": {
    "dietary_restrictions": [str],    # e.g., ["vegetarian", "vegan"]
    "allergens": [str],               # e.g., ["peanuts", "shellfish"]
    "cuisine_preferences": [str],     # e.g., ["Italian", "Mexican"]
    "spice_level": str | None         # "mild", "medium", "hot"
  },
  "social_media": {
    "facebook": str | None,
    "instagram": str | None,
    "twitter": str | None
  },
  "role": str,                        # "user" | "admin"
  "status": str,                      # "pending" | "active" | "suspended" | "rejected"
  "stats": {
    "total_meals_sold": int,
    "total_meals_swapped": int,
    "total_meals_purchased": int,
    "average_rating": float,
    "total_reviews": int,
    "badges": [Badge]
  },
  "verified": bool,                   # Email verification status
  "created_at": datetime,             # Account creation timestamp
  "updated_at": datetime              # Last update timestamp
}
```

### Meal Data Model

```python
{
  "_id": ObjectId,                    # MongoDB document ID
  "seller_id": ObjectId,              # Reference to user document
  "title": str,                       # Meal title (3-100 chars)
  "description": str,                 # Meal description (10-1000 chars)
  "cuisine_type": str,                # e.g., "Italian", "Mexican", "Asian"
  "meal_type": str,                   # e.g., "breakfast", "lunch", "dinner"
  "photos": [str],                    # Array of photo URLs
  "allergen_info": {
    "contains": [str],                # Definite allergens
    "may_contain": [str]              # Possible cross-contamination
  },
  "nutrition_info": {                 # Optional nutrition data
    "calories": int | None,
    "protein_grams": float | None,
    "carbs_grams": float | None,
    "fat_grams": float | None
  },
  "portion_size": str,                # e.g., "Serves 4", "1 portion"
  "available_for_sale": bool,         # Can be purchased
  "sale_price": float | None,         # Price in USD
  "available_for_swap": bool,         # Can be swapped
  "swap_preferences": [str],          # Desired swap items
  "status": str,                      # "available" | "pending" | "sold" | "swapped" | "unavailable"
  "preparation_date": datetime,       # When meal was prepared
  "expires_date": datetime,           # When meal expires
  "pickup_instructions": str | None,  # Pickup details
  "average_rating": float,            # Average rating (0.0-5.0)
  "total_reviews": int,               # Number of reviews
  "views": int,                       # View count
  "created_at": datetime,             # Creation timestamp
  "updated_at": datetime              # Last update timestamp
}
```

### Verification Token Data Model

```python
{
  "_id": ObjectId,
  "email": str,                       # Email to verify
  "token": str,                       # Random verification token
  "token_type": str,                  # "email_verification" | "password_reset"
  "expires_at": datetime,             # Token expiration (24 hours)
  "created_at": datetime
}
```

### Review Data Model

```python
{
  "_id": ObjectId,
  "meal_id": ObjectId,                # Reference to meal
  "reviewer_id": ObjectId,            # Reference to reviewer
  "seller_id": ObjectId,              # Reference to seller
  "rating": int,                      # 1-5 stars
  "comment": str | None,              # Optional review text (max 500 chars)
  "transaction_type": str,            # "sale" | "swap"
  "verified_transaction": bool,       # Is this from actual transaction
  "created_at": datetime
}
```

### Badge Data Model

```python
{
  "badge_type": str,                  # "verified_seller" | "top_chef" | "five_star" 
                                      # | "community_favorite" | "swap_master"
  "earned_date": datetime,            # When badge was earned
  "description": str                  # Badge description
}
```

---

## Security Best Practices

### Current Implementation Notes

⚠️ **Important:** The current authentication implementation uses email as Bearer token. This is **NOT production-ready**. 

### Recommended Production Changes

#### 1. Implement JWT Authentication

Replace the current authentication in `dependencies.py`:

```python
from jose import JWTError, jwt
from datetime import datetime, timedelta

SECRET_KEY = "your-secret-key-here"  # Use environment variable
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    db = get_database()
    user = await db.users.find_one({"email": email})
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user
```

#### 2. Use Environment Variables

Never hardcode sensitive information:

```python
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
MONGODB_URL = os.getenv("MONGODB_URL")
EMAIL_API_KEY = os.getenv("EMAIL_API_KEY")
```

#### 3. Implement Rate Limiting

Protect against brute force attacks:

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.post("/api/auth/login")
@limiter.limit("5/minute")
async def login(request: Request, credentials: UserLogin):
    # Login logic
    pass
```

#### 4. Add HTTPS in Production

Use reverse proxy (nginx) with SSL certificates:

```nginx
server {
    listen 443 ssl;
    server_name api.tastebuddies.com;
    
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    
    location / {
        proxy_pass http://localhost:8000;
    }
}
```

#### 5. Password Security

Current implementation uses bcrypt (good). Ensure:
- Minimum 8 characters
- Complexity requirements enforced
- Maximum 72 characters (bcrypt limit)
- Password history to prevent reuse

#### 6. Input Validation

Always validate and sanitize inputs:
- Use Pydantic models (already implemented)
- Validate ObjectIds before database queries
- Sanitize user-generated content
- Implement file upload validation if adding image uploads

#### 7. Database Security

- Use connection string with authentication in production
- Implement role-based access control (RBAC)
- Enable MongoDB authentication
- Use connection pooling
- Regular backups

```python
MONGODB_URL = "mongodb://username:password@mongodb:27017/tastebuddies?authSource=admin"
```

---

## Performance Optimization

### Database Indexing

Indexes are automatically created. Monitor query performance:

```javascript
// In MongoDB shell
db.meals.find({cuisine_type: "Italian"}).explain("executionStats")
```

### Caching Strategies

Consider implementing caching for:
- Popular meal listings
- User profiles
- Cuisine type filters

Example with Redis:

```python
import redis
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

@app.on_event("startup")
async def startup():
    redis_client = redis.from_url("redis://localhost:6379")
    FastAPICache.init(RedisBackend(redis_client), prefix="tastebuddies-cache")

@app.get("/api/meals/")
@cache(expire=300)  # Cache for 5 minutes
async def get_meals():
    # Endpoint logic
    pass
```

### Pagination Best Practices

Always implement pagination for list endpoints:

```python
# Good
GET /api/meals/?skip=0&limit=20

# Avoid
GET /api/meals/  # Returns all meals
```

### Image Optimization

For meal photos:
- Store images in CDN (AWS S3, Cloudflare)
- Implement image resizing
- Use lazy loading on frontend
- Compress images before upload

---

## Testing Guide

### Running Tests

```bash
# Run all tests
docker-compose up backend-tests

# Run specific test file
docker-compose run backend-tests pytest tests/test_auth.py

# Run with coverage
docker-compose run backend-tests pytest --cov=app tests/

# Run with verbose output
docker-compose run backend-tests pytest -v -s
```

### Test Structure

```
tests/
├── __init__.py
├── conftest.py           # Shared fixtures
├── test_auth.py          # Authentication tests
├── test_users.py         # User endpoint tests
├── test_meals.py         # Meal endpoint tests
└── test_database.py      # Database operation tests
```

### Writing Tests

Example test file:

```python
import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_register_user():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/api/auth/register/user", json={
            "email": "test@example.com",
            "password": "TestPass123",
            "full_name": "Test User",
            "location": {
                "address": "123 Test St",
                "city": "Raleigh",
                "state": "NC",
                "zip_code": "27601"
            }
        })
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == "test@example.com"

@pytest.mark.asyncio
async def test_login_user():
    async with AsyncClient(app=app, base_url="http://test") as client:
        # First register
        await client.post("/api/auth/register/user", json={...})
        
        # Then login
        response = await client.post("/api/auth/login", json={
            "email": "test@example.com",
            "password": "TestPass123"
        })
        assert response.status_code == 200
        assert "user_id" in response.json()
```

---

## Deployment to Production

### Production Checklist

- [ ] Replace email-based authentication with JWT
- [ ] Set up environment variables for secrets
- [ ] Configure HTTPS/SSL certificates
- [ ] Set up MongoDB with authentication
- [ ] Implement rate limiting
- [ ] Configure CORS for specific domains
- [ ] Set up logging and monitoring
- [ ] Configure automated backups
- [ ] Set up CI/CD pipeline
- [ ] Implement error tracking (Sentry, etc.)
- [ ] Configure email service (SendGrid, AWS SES)
- [ ] Set up CDN for static assets
- [ ] Implement health checks and monitoring
- [ ] Configure firewall rules
- [ ] Set up load balancing (if needed)

### Docker Production Build

Create `docker-compose.prod.yml`:

```yaml
version: '3.8'

services:
  backend:
    build: .
    environment:
      - MONGODB_URL=${MONGODB_URL}
      - SECRET_KEY=${SECRET_KEY}
      - DATABASE_NAME=tastebuddies_prod
    restart: always
    
  mongodb:
    image: mongo:latest
    environment:
      - MONGO_INITDB_ROOT_USERNAME=${MONGO_USER}
      - MONGO_INITDB_ROOT_PASSWORD=${MONGO_PASSWORD}
    volumes:
      - mongodb_data:/data/db
    restart: always
    
  nginx:
    image: nginx:alpine
    ports:
      - "443:443"
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - backend
    restart: always

volumes:
  mongodb_data:
```

### Environment Variables for Production

Create `.env.production`:

```env
# MongoDB
MONGODB_URL=mongodb://username:password@mongodb:27017/tastebuddies_prod?authSource=admin
DATABASE_NAME=tastebuddies_prod
MONGO_USER=admin
MONGO_PASSWORD=secure_password_here

# Security
SECRET_KEY=your-very-secure-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Email Service
EMAIL_API_KEY=your-email-service-api-key
EMAIL_FROM=noreply@tastebuddies.com

# Application
ENVIRONMENT=production
DEBUG=false
```

### Monitoring and Logging

Implement structured logging:

```python
import logging
from pythonjsonlogger import jsonlogger

logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter()
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info("request_started", extra={
        "method": request.method,
        "path": request.url.path,
        "client": request.client.host
    })
    response = await call_next(request)
    logger.info("request_completed", extra={
        "status_code": response.status_code
    })
    return response
```

---

## API Versioning

Future versions should implement API versioning:

```python
# v1 routes
app.include_router(auth_router, prefix="/api/v1", tags=["Auth v1"])
app.include_router(user_router, prefix="/api/v1", tags=["Users v1"])

# v2 routes (with breaking changes)
app.include_router(auth_router_v2, prefix="/api/v2", tags=["Auth v2"])
```

---

## Contributing Guidelines

### Code Style

- Follow PEP 8 for Python code
- Use type hints where possible
- Write docstrings for functions
- Keep functions focused and small
- Maximum line length: 100 characters

### Git Workflow

1. Create feature branch: `git checkout -b feature/meal-swapping`
2. Make changes and commit: `git commit -m "Add meal swap endpoint"`
3. Push to GitHub: `git push origin feature/meal-swapping`
4. Create Pull Request
5. Wait for code review and CI checks
6. Merge after approval

### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No new warnings generated
```

---

## License and Support

### License
This project is part of CSC510 coursework. Please refer to the repository for licensing information.

### Support Channels
- **GitHub Issues:** https://github.com/madisonbook/CSC510/issues
- **Documentation:** This file
- **API Docs:** http://localhost:8000/docs

### Version History

- **v1.0.0** (Current) - Initial release with core functionality
  - User authentication and registration
  - Meal listing and management
  - Basic search and filtering

---

**Last Updated:** October 22, 2024  
**Documentation Version:** 1.0.0