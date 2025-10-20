# Group 26

[![Syntax Check](https://github.com/madisonbook/CSC510/actions/workflows/syntax-check.yml/badge.svg?branch=alicebadges)](https://github.com/madisonbook/CSC510/actions/workflows/syntax-check.yml)

[![Code Coverage](https://codecov.io/gh/madisonbook/CSC510/branch/alicebadges/graph/badge.svg)](https://codecov.io/gh/madisonbook/CSC510)

# 1. Install Prerequisites
- Docker Desktop
- Docker Compose

# 2. Docker Commands

### Build and start all services
docker-compose up --build

### Run in detached mode
docker-compose up -d --build

### Run backend tests
docker-compose up --build backend-tests

### Stop all services
docker-compose down

### Stop and remove volumes (clears database)
docker-compose down -v

### View logs
docker-compose logs -f

### View logs for specific service
docker-compose logs -f backend

### Restart a service
docker-compose restart backend

### Execute commands in container
docker-compose exec backend bash
docker-compose exec mongodb mongosh
