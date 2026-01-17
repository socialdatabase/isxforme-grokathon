#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${GREEN}Starting Rapid Django Vue setup...${NC}"

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "Docker is not running. Please start Docker and try again."
    exit 1
fi

# Check if .env file exists, if not create it from example
if [ ! -f .env ]; then
    echo -e "${YELLOW}No .env file found. Creating from .env.example...${NC}"
    if [ -f .env.example ]; then
        cp .env.example .env
        echo -e "${GREEN}✓ Created .env file${NC}"
        echo -e "${BLUE}ℹ  For production, remember to update SECRET_KEY, DEBUG, and passwords in .env${NC}"
    else
        echo -e "${YELLOW}⚠ Warning: .env.example not found. Please create .env manually.${NC}"
    fi
else
    echo -e "${BLUE}ℹ .env file already exists, skipping...${NC}"
fi

echo -e "${YELLOW}Building and starting containers...${NC}"
docker-compose up --build -d

echo -e "${YELLOW}Waiting for database to be ready...${NC}"
sleep 5

echo -e "${YELLOW}Running database migrations...${NC}"
docker-compose exec backend python manage.py migrate

echo -e "${GREEN}Setup complete!${NC}"
echo ""
echo "Services are running at:"
echo "  Frontend: http://localhost:3000"
echo "  Backend API: http://localhost:8000/api"
echo "  Django Admin: http://localhost:8000/admin"
echo ""
echo "To create a superuser, run:"
echo "  docker-compose exec backend python manage.py createsuperuser"
echo ""
echo "To view logs:"
echo "  docker-compose logs -f"
echo ""
echo "To stop services:"
echo "  docker-compose down"

