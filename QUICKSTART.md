# Quick Start Guide

## Get Up and Running in 3 Minutes

### Prerequisites
- Docker and Docker Compose installed
- Git

### Manual Setup

1. **Clone the repository:**
```bash
git clone https://github.com/yourusername/grokathon.git
cd grokathon
```

2. **Set up environment variables:**
```bash
cp .env.example .env
```
*Note: Default values work for development. For production, edit .env and update DEBUG, SECRET_KEY, passwords, and URLs!*

3. **Start the services:**
```bash
docker-compose up --build
```

4. **In a new terminal, run migrations:**
```bash
docker-compose exec backend python manage.py migrate
```

5. **Create an admin user (optional):**
```bash
docker-compose exec backend python manage.py createsuperuser
```

### Using the Setup Script (Automated)

The setup scripts will automatically copy `.env.example` to `.env` if it doesn't exist.

**On macOS/Linux:**
```bash
./setup.sh
```

**On Windows:**
```bash
setup.bat
```

## What's Running?

-  **Frontend**: http://localhost:3000
-  **Backend API**: http://localhost:8000/api
-  **Django Admin**: http://localhost:8000/admin
- ️ **PostgreSQL**: localhost:5432

## Test the Application

1. Open http://localhost:3000
2. Click "Register" and create an account
3. Login with your credentials
4. View your dashboard with your user information

## Using Makefile Commands

If you have `make` installed:

```bash
make build          # Build containers
make up             # Start services
make down           # Stop services
make logs           # View logs
make migrate        # Run migrations
make createsuperuser # Create admin user
```

## Stopping the Application

```bash
docker-compose down
```

## Troubleshooting

### Port Already in Use
If you get port conflicts, modify the ports in `docker-compose.yml`.

### Database Connection Issues
Wait a few seconds after starting for the database to be ready, then run migrations.

### Frontend Can't Connect to Backend
Check that both services are running:
```bash
docker-compose ps
```

## Next Steps

- Read the full [README.md](README.md)
- Customize the frontend in `frontend/src/`
- Add new API endpoints in `backend/`
- Deploy to production (see README.md)

---

Need help? Check the [README.md](README.md) or open an issue on GitHub.

