[![Syntax Check](https://github.com/madisonbook/CSC510/actions/workflows/syntax-check.yml/badge.svg?branch=alicebadges)](https://github.com/madisonbook/CSC510/actions/workflows/syntax-check.yml)

[![Code Coverage](https://codecov.io/gh/madisonbook/CSC510/branch/alicebadges/graph/badge.svg)](https://codecov.io/gh/madisonbook/CSC510)

# TASTE BUDDIEZ (Group 26)

## Our Story

* **Tired of eating the same meal for a week straight?**
* **Want to take your home cooking to the next level?**
* **Craving some authentic local cuisine?**

At Taste Buddiez, we believe food is more than just fuel — it’s a connection. Our mission is to bring neighbors together through the flavors they create and love. Whether you’re a busy professional craving home-cooked variety, a local chef eager to share your craft, or a foodie seeking authentic dishes from your own community, Taste Buddiez makes it simple to buy, sell, and swap homemade meals right in your neighborhood.

## Quick Start Guide

### 0. Prerequisites
Ensure you have the following installed
1. Git (for cloning the repository)
2. Docker & docker-compose (for running the application)
3. Docker Desktop (for viewing containers)

### 1. Clone the Repository
1. navigate to the directory where you want to store the software
2. terminal: 'git clone https://github.com/madisonbook/CSC510.git'
3. terminal: 'cd CSC510'

### 2. Build and Run the Application
1. terminal: 'cd proj2'
2. terminal: 'docker-compose up --build'
3. navigate to [http://localhost:5173/](http://localhost:5173/) in your browser

### 3. Stopping the Application
1. terminal: 'Ctrl+C' OR 'docker-compose down'

### 4. Build and Run Backend Tests
1. terminal: 'docker-compose up --build backend-tests'

### 5. Other Docker Commands
1. Run in detached mode: 'docker-compose up -d --build'
2. Stop application and remove volumes: 'docker-compose down -v'
3. View logs: 'docker-compose logs -f'
4. Restart a service: 'docker-compose restart {ie. backend}'
