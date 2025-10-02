Group 26

### 1. Install Prerequisites
- Docker Desktop
- Docker Compose

### 2. Docker Commands

# Build and start all services
docker-compose up --build

# Or run in detached mode
docker-compose up -d --build

# Stop all services
docker-compose down

# Stop and remove volumes (clears database)
docker-compose down -v

# View logs
docker-compose logs -f

# View logs for specific service
docker-compose logs -f backend

# Restart a service
docker-compose restart backend

# Execute commands in container
docker-compose exec backend bash
docker-compose exec mongodb mongosh
