# Taste Buddies - Deployment Guide

**Version:** 1.0.0

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Step-by-Step Deployment](#step-by-step-deployment)
3. [Stopping the Application](#stopping-the-application)
4. [Running Tests](#running-tests)
5. [Docker Commands Reference](#docker-commands-reference)
6. [Local Development Setup](#local-development-setup)

---

## Prerequisites

Before deploying Taste Buddies, ensure you have:

### 1. Git (version 2.0+)
- **Download:** https://git-scm.com/downloads
- **Verify Installation:**
  ```bash
  git --version
  ```

### 2. Docker (version 20.0+)
- **Download:** https://docs.docker.com/get-docker/
- **Verify Installation:**
  ```bash
  docker --version
  ```

### 3. Docker Compose (version 2.0+)
- **Included with Docker Desktop**
- **Verify Installation:**
  ```bash
  docker-compose --version
  ```

### 4. Docker Desktop (Recommended)
- **Download:** https://www.docker.com/products/docker-desktop
- **Purpose:** Visual container management and monitoring

---

## Step-by-Step Deployment

### Step 1: Clone the Repository

```bash
# Navigate to your desired directory
cd /path/to/your/workspace

# Clone the repository
git clone https://github.com/madisonbook/CSC510.git

# Navigate into the project
cd CSC510
```

### Step 2: Navigate to Project Directory

```bash
cd proj2
```

### Step 3: Configure Environment Variables (Optional)

Create a `.env` file in the `proj2` directory if you need custom configuration:

```env
MONGODB_URL=mongodb://mongodb:27017
DATABASE_NAME=tastebuddies
```

### Step 4: Build and Start the Application

```bash
# Build and start all services
docker-compose up --build
```

**What happens during startup:**
- MongoDB container starts on port 27017
- Backend API starts on port 8000
- Frontend starts on port 5173
- Database indexes are automatically created
- All services connect and initialize

**Expected Output:**
```
✅ Connected to MongoDB at mongodb://mongodb:27017
✅ Database indexes verified/created
✅ Application running on http://0.0.0.0:8000
```

### Step 5: Access the Application

Open your browser and navigate to:

- **Frontend Application:** http://localhost:5173
- **API Documentation (Swagger):** http://localhost:8000/docs
- **Alternative API Docs (ReDoc):** http://localhost:8000/redoc
- **Health Check Endpoint:** http://localhost:8000/health

### Step 6: Verify Installation

Check that all services are running:

```bash
docker-compose ps
```

**Expected Output:**
```
NAME                COMMAND                  SERVICE      STATUS
proj2-backend-1     uvicorn app.main:app ... backend      Up
proj2-frontend-1    npm start                frontend     Up
proj2-mongodb-1     mongod                   mongodb      Up
```

You should see three services with status "Up":
- `mongodb`
- `backend`
- `frontend`

---

## Stopping the Application

### Option 1: Stop with Ctrl+C

If running in foreground:
```bash
# Press Ctrl+C in the terminal
```

### Option 2: Stop Services (Keep Data)

```bash
# Stop all services but preserve data volumes
docker-compose down
```

### Option 3: Complete Cleanup

```bash
# Stop services and remove all volumes (deletes all data)
docker-compose down -v
```

**Warning:** Using `-v` flag will delete all database data permanently.

---

## Running Tests

### Backend Tests

```bash
# Run the complete test suite
docker-compose up --build backend-tests
```

### Run Specific Test File

```bash
# Run authentication tests only
docker-compose run backend-tests pytest tests/test_auth.py

# Run with verbose output
docker-compose run backend-tests pytest tests/test_auth.py -v

# Run with coverage report
docker-compose run backend-tests pytest --cov=app tests/
```

### View Test Results

After running tests, you'll see:
- Test pass/fail status
- Code coverage percentage
- Execution time
- Any errors or warnings

---

## Docker Commands Reference

### Running in Detached Mode (Background)

```bash
# Start services in background
docker-compose up -d --build

# View logs from all services
docker-compose logs -f

# View logs from specific service
docker-compose logs -f backend

# Stop background services
docker-compose down
```

### Rebuilding Services

```bash
# Rebuild without cache (useful after dependency changes)
docker-compose build --no-cache

# Rebuild specific service
docker-compose build backend
```

### Managing Services

```bash
# Restart a specific service
docker-compose restart backend

# Stop a specific service
docker-compose stop mongodb

# Start a stopped service
docker-compose start mongodb

# View service resource usage
docker stats
```

### Database Management

```bash
# Access MongoDB shell
docker exec -it proj2-mongodb-1 mongosh

# Backup database
docker exec proj2-mongodb-1 mongodump --out /backup

# View container details
docker inspect proj2-backend-1
```

### Cleaning Up

```bash
# Remove stopped containers
docker-compose rm

# Remove all unused containers, networks, images
docker system prune

# Remove everything including volumes (CAUTION: deletes data)
docker system prune -a --volumes
```

---

## Local Development Setup

### Without Docker

If you prefer to run the application locally without Docker:

#### 1. Install Python 3.11+

Download from: https://www.python.org/downloads/

Verify:
```bash
python --version
```

#### 2. Install Dependencies

```bash
cd proj2
pip install -r requirements.txt
```

#### 3. Start MongoDB

**Option A: Using Docker**
```bash
docker run -d -p 27017:27017 --name mongodb mongo:latest
```

**Option B: Install MongoDB locally**
- Download: https://www.mongodb.com/try/download/community
- Follow installation instructions for your OS

#### 4. Set Environment Variables

**Linux/Mac:**
```bash
export MONGODB_URL=mongodb://localhost:27017
export DATABASE_NAME=tastebuddies
```

**Windows (Command Prompt):**
```cmd
set MONGODB_URL=mongodb://localhost:27017
set DATABASE_NAME=tastebuddies
```

**Windows (PowerShell):**
```powershell
$env:MONGODB_URL="mongodb://localhost:27017"
$env:DATABASE_NAME="tastebuddies"
```

#### 5. Run the Application

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The `--reload` flag enables auto-reload on code changes for development.

#### 6. Access the Application

- **API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs

---

## Environment Variables

### Available Configuration Options

| Variable | Default | Description |
|----------|---------|-------------|
| `MONGODB_URL` | `mongodb://mongodb:27017` | MongoDB connection string |
| `DATABASE_NAME` | `myapp` | Database name to use |

### Creating a .env File

Create a `.env` file in the `proj2` directory:

```env
# MongoDB Configuration
MONGODB_URL=mongodb://mongodb:27017
DATABASE_NAME=tastebuddies

# API Configuration (for future use)
SECRET_KEY=your-secret-key-here
ENVIRONMENT=development
DEBUG=true
```

**Note:** Never commit `.env` files with sensitive data to version control.

---

## Deployment Architecture

### Container Structure

```
┌─────────────────────────────────────┐
│         Docker Network              │
│                                     │
│  ┌──────────┐  ┌──────────┐       │
│  │ Frontend │  │ Backend  │       │
│  │  :5173   │  │  :8000   │       │
│  └────┬─────┘  └────┬─────┘       │
│       │             │              │
│       └─────┬───────┘              │
│             │                      │
│       ┌─────▼──────┐              │
│       │  MongoDB   │              │
│       │   :27017   │              │
│       └────────────┘              │
└─────────────────────────────────────┘
```

### Service Dependencies

- **Frontend** depends on **Backend**
- **Backend** depends on **MongoDB**
- Services start in order of dependencies

---

## Port Configuration

### Default Ports

- **Frontend:** 5173
- **Backend API:** 8000
- **MongoDB:** 27017

### Changing Ports

Edit `docker-compose.yml`:

```yaml
services:
  backend:
    ports:
      - "8080:8000"  # Change host port from 8000 to 8080
  
  frontend:
    ports:
      - "3000:5173"  # Change host port from 5173 to 3000
```

---

## Verifying Successful Deployment

### Health Check

```bash
curl http://localhost:8000/health
```

**Expected Response:**
```json
{
  "status": "healthy"
}
```

### API Root

```bash
curl http://localhost:8000/
```

**Expected Response:**
```json
{
  "message": "Welcome to Taste Buddiez API",
  "tagline": "Connecting neighbors through homemade meals"
}
```

### Check Database Connection

```bash
# Access MongoDB
docker exec -it proj2-mongodb-1 mongosh

# Inside MongoDB shell
show dbs
use tastebuddies
show collections
```

---

## Production Deployment Notes

### Security Considerations

For production deployment:

1. **Use HTTPS** - Configure SSL/TLS certificates
2. **Set Strong Secrets** - Use environment variables for sensitive data
3. **Enable Authentication** - Configure MongoDB authentication
4. **Implement Rate Limiting** - Protect against abuse
5. **Configure CORS** - Restrict to specific domains

### Production Checklist

- [ ] Configure environment variables
- [ ] Set up SSL certificates
- [ ] Enable MongoDB authentication
- [ ] Configure firewall rules
- [ ] Set up automated backups
- [ ] Configure monitoring and logging
- [ ] Test disaster recovery procedures
- [ ] Review security settings
- [ ] Configure rate limiting
- [ ] Set up CI/CD pipeline

### Recommended Production Setup

```yaml
# docker-compose.prod.yml
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

volumes:
  mongodb_data:
```

---

## Troubleshooting Deployment

### Services Won't Start

1. **Check Docker is running:**
   ```bash
   docker info
   ```

2. **Check for port conflicts:**
   ```bash
   lsof -i :8000
   lsof -i :5173
   ```

3. **View error logs:**
   ```bash
   docker-compose logs
   ```

### Database Connection Issues

1. **Verify MongoDB is running:**
   ```bash
   docker-compose ps mongodb
   ```

2. **Check MongoDB logs:**
   ```bash
   docker-compose logs mongodb
   ```

3. **Test connection:**
   ```bash
   docker exec -it proj2-mongodb-1 mongosh
   ```

For more detailed troubleshooting, see [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

---

**Last Updated:** October 22, 2024  
**Documentation Version:** 1.0.0