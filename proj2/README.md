[![Syntax Check](https://github.com/madisonbook/CSC510/actions/workflows/syntax-check.yml/badge.svg?branch=alicebadges)](https://github.com/madisonbook/CSC510/actions/workflows/syntax-check.yml)

[![Code Coverage](https://codecov.io/gh/madisonbook/CSC510/branch/development/graph/badge.svg)](https://codecov.io/gh/madisonbook/CSC510)

[![Run Tests](https://github.com/madisonbook/CSC510/actions/workflows/backend-tests.yml/badge.svg)](https://github.com/madisonbook/CSC510/actions/workflows/backend-tests.yml)

![Code Format](https://github.com/madisonbook/CSC510/actions/workflows/format.yml/badge.svg)

# TASTE BUDDIEZ (Group 26)

## Our Story

* **Tired of eating the same meal for a week straight?**
* **Want to take your home cooking to the next level?**
* **Craving some authentic local cuisine?**

At Taste Buddiez, we believe food is more than just fuel — it’s a connection. Our mission is to bring neighbors together through the flavors they create and love. Whether you’re a busy professional craving home-cooked variety, a local chef eager to share your craft, or a foodie seeking authentic dishes from your own community, Taste Buddiez makes it simple to buy, sell, and swap homemade meals right in your neighborhood.

## Our Product

### Taste Buddies is a neighborhood meal-sharing platform that allows users to:
* List homemade meals for sale or swap
* Discover meals from local home cooks
* Build community through food sharing
* Review and rate meals

### Technology Stack:
* Backend: FastAPI (Python)
* Database: MongoDB
* Frontend: React (Port 5173)
* Containerization: Docker & Docker Compose

## Quick Start Guide

## Prerequisites

Before you begin, ensure you have the following installed:

1. **Docker Desktop** (version 20.0+)
   - Download: https://www.docker.com/products/docker-desktop
   - Required for running the application containers
   - Verify installation: `docker --version`

2. **Python** (version 3.8+)
   - Download: https://www.python.org/downloads/
   - Required for running the CLI package
   - Verify installation: `python --version`

3. **Git** (version 2.0+)
   - Download: https://git-scm.com/downloads/
   - Required for cloning the repository
   - Verify installation: `git --version`

## Installation & Setup

### Step 1: Clone the Repository

```bash
# Clone the repository
git clone https://github.com/madisonbook/CSC510.git

# Navigate to the project directory
cd CSC510/proj2
```

### Step 2: Install the TasteBuddiez CLI Package

The application uses a custom CLI package for easy management. Install it in editable mode:

```bash
pip install -e .
```

**Note for Windows PowerShell users:** If you get a "command not recognized" error after installation, the script isn't on your PATH. Use one of these alternatives:

**Option A - Run directly via Python:**
```powershell
python tastebuddiez\cli.py start
```

**Option B - Add Python Scripts to PATH:**
The installation will show a warning like:
```
WARNING: The script tastebuddiez.exe is installed in 'C:\Users\...\Python311\Scripts' which is not on PATH.
```
Add that directory to your system PATH, then you can use `tastebuddiez start` directly.

### Step 3: Start the Application

```bash
# Start all services (MongoDB, Backend, Frontend)
python tastebuddiez\cli.py start
```

Or with additional options:
```bash
# Rebuild images before starting
python tastebuddiez\cli.py start --build

# Run in detached mode (background)
python tastebuddiez\cli.py start --detach
```

The application will start three services:
- **MongoDB** - Database (port 27017)
- **FastAPI Backend** - REST API (port 8000)
- **React Frontend** - Web interface (port 5173)

### Step 4: Access the Application

Once all services are running (you'll see "✔ Container ... Running" messages):

- **Frontend Application:** http://localhost:5173
- **Backend API Docs:** http://localhost:8000/docs
- **Backend API:** http://localhost:8000

## CLI Commands Reference

The `tastebuddiez` CLI provides several commands for managing the application:

```bash
# Start the application
python tastebuddiez\cli.py start [--build] [--detach]

# Stop the application
python tastebuddiez\cli.py stop

# Restart the application
python tastebuddiez\cli.py restart

# View logs from all services
python tastebuddiez\cli.py logs

# Check status of all services
python tastebuddiez\cli.py status

# Run tests
python tastebuddiez\cli.py test [all|meals|users|main] [--build] [--coverage]

# Clean up (remove all data and volumes)
python tastebuddiez\cli.py clean

# Setup development environment
python tastebuddiez\cli.py setup
```

## Running Tests

Run the test suite to verify everything is working:

```bash
# Run all tests
python tastebuddiez\cli.py test all

# Run specific test suites
python tastebuddiez\cli.py test meals
python tastebuddiez\cli.py test users
python tastebuddiez\cli.py test main

# Run tests with coverage report
python tastebuddiez\cli.py test all --coverage

# Rebuild containers before running tests
python tastebuddiez\cli.py test all --build
```

## Stopping the Application

To stop all services:

```bash
python tastebuddiez\cli.py stop
```

To stop and remove all data (clean slate):

```bash
python tastebuddiez\cli.py clean
```

## Troubleshooting

### "Command not recognized" Error (Windows)
If you get `tastebuddiez : The term 'tastebuddiez' is not recognized`:
- Use `python tastebuddiez\cli.py` instead of `tastebuddiez`
- Or add the Python Scripts directory to your PATH

### "Could not find docker-compose.yml" Error
Make sure you're running commands from the `proj2` directory:
```bash
cd CSC510/proj2
python tastebuddiez\cli.py start
```

### Port Already in Use
If ports 5173, 8000, or 27017 are already in use:
1. Stop the conflicting services
2. Or modify the ports in `docker-compose.yml`

### Docker Not Running
Make sure Docker Desktop is running before starting the application.

### Containers Won't Start
Try rebuilding the containers:
```bash
python tastebuddiez\cli.py stop
python tastebuddiez\cli.py start --build
```

## Development Workflow

### Making Code Changes

**Backend Changes:**
- Edit files in `backend/app/`
- Changes are automatically reflected (hot reload enabled)
- Backend runs on http://localhost:8000

**Frontend Changes:**
- Edit files in `frontend/src/`
- Changes trigger automatic rebuild (Vite HMR)
- Frontend runs on http://localhost:5173

### Viewing Logs

```bash
# View all service logs
python tastebuddiez\cli.py logs

# Or use Docker commands for specific services
docker logs fastapi-backend
docker logs react-frontend
docker logs mongodb
```

### Database Access

MongoDB is accessible at `localhost:27017`

You can connect using:
- MongoDB Compass: `mongodb://localhost:27017`
- mongosh: `mongosh mongodb://localhost:27017/myapp`

## Project Structure

```
proj2/
├── backend/              # FastAPI backend
│   ├── app/             # Application code
│   ├── tests/           # Backend tests
│   └── requirements.txt # Python dependencies
├── frontend/            # React frontend
│   ├── src/            # Source code
│   └── package.json    # Node dependencies
├── tastebuddiez/       # CLI package
│   └── cli.py          # Command-line interface
├── docker-compose.yml  # Docker services configuration
└── setup.py           # Package setup
```

## Additional Resources

- **Deployment Guide:** `documentation/taste-buddies-deployment-guide.md`
- **API Reference:** `documentation/taste-buddies-api-reference.md`
- **Development Guide:** `documentation/taste-buddies-development-guide.md`
- **Troubleshooting:** `documentation/taste-buddies-troubleshooting.md`

## Quick Reference

```bash
# First time setup
git clone https://github.com/madisonbook/CSC510.git
cd CSC510/proj2
pip install -e .

# Daily usage
python tastebuddiez\cli.py start     # Start app
# ... work on your code ...
python tastebuddiez\cli.py stop      # Stop app

# Testing
python tastebuddiez\cli.py test all  # Run tests
```

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review documentation in the `documentation/` folder
3. Check Docker Desktop to verify containers are running
4. View logs with `python tastebuddiez\cli.py logs`
