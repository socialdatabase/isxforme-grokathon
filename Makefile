# Makefile for Rapid Django Vue

.PHONY: help build up down restart logs migrate makemigrations createsuperuser shell test clean

help:
	@echo "Rapid Django Vue - Available commands:"
	@echo "  make build          - Build Docker containers"
	@echo "  make up             - Start all services"
	@echo "  make down           - Stop all services"
	@echo "  make restart        - Restart all services"
	@echo "  make logs           - View logs"
	@echo "  make migrate        - Run Django migrations"
	@echo "  make makemigrations - Create Django migrations"
	@echo "  make createsuperuser - Create Django superuser"
	@echo "  make shell          - Open Django shell"
	@echo "  make test           - Run tests"
	@echo "  make clean          - Remove containers and volumes"

build:
	docker-compose build

up:
	docker-compose up -d
	@echo "Services started!"
	@echo "Frontend: http://localhost:8080"
	@echo "Backend: http://localhost:8000"

down:
	docker-compose down

restart:
	docker-compose restart

logs:
	docker-compose logs -f

migrate:
	docker-compose exec backend python manage.py migrate

makemigrations:
	docker-compose exec backend python manage.py makemigrations

createsuperuser:
	docker-compose exec backend python manage.py createsuperuser

shell:
	docker-compose exec backend python manage.py shell

test:
	docker-compose exec backend python manage.py test
	docker-compose exec frontend npm run test

clean:
	docker-compose down -v
	@echo "Cleaned up containers and volumes"

