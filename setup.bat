@echo off
echo Starting Rapid Django Vue setup...

docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo Docker is not running. Please start Docker and try again.
    exit /b 1
)

REM Check if .env file exists, if not create it from example
if not exist .env (
    echo No .env file found. Creating from .env.example...
    if exist .env.example (
        copy .env.example .env >nul
        echo Created .env file
        echo For production, remember to update SECRET_KEY, DEBUG, and passwords in .env
    ) else (
        echo Warning: .env.example not found. Please create .env manually.
    )
) else (
    echo .env file already exists, skipping...
)

echo Building and starting containers...
docker-compose up --build -d

echo Waiting for database to be ready...
timeout /t 5 /nobreak >nul

echo Running database migrations...
docker-compose exec backend python manage.py migrate

echo.
echo Setup complete!
echo.
echo Services are running at:
echo   Frontend: http://localhost:3000
echo   Backend API: http://localhost:8000/api
echo   Django Admin: http://localhost:8000/admin
echo.
echo To create a superuser, run:
echo   docker-compose exec backend python manage.py createsuperuser
echo.
echo To view logs:
echo   docker-compose logs -f
echo.
echo To stop services:
echo   docker-compose down

