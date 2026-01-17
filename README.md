# Rapid Django Nuxt

A modern, production-ready boilerplate for building web applications with Django REST Framework backend and Nuxt 3 frontend, featuring JWT authentication and Docker support.

**Built by [@thomasslabbers](https://x.com/thomasslabbers)** · Follow on [𝕏](https://x.com/thomasslabbers)

## Features

- **Django 4.2** - Modern Python web framework
- **Django REST Framework** - Powerful toolkit for building Web APIs
- **Nuxt 3** - The Intuitive Vue Framework with SSR/SSG support
- **JWT Authentication** - Secure token-based authentication with djangorestframework-simplejwt
- **Pinia** - State management for Vue
- **Docker & Docker Compose** - Easy development and deployment
- **PostgreSQL** - Robust relational database
- **CORS Support** - Configured for cross-origin requests
- **TypeScript Ready** - Modern development experience
- **Modern UI** - Clean and responsive user interface

## Project Structure

```
Rapid-Django-Nuxt/
├── backend/                 # Django backend
│   ├── config/             # Django project settings
│   ├── users/              # User authentication app
│   ├── manage.py
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/               # Nuxt 3 frontend
│   ├── pages/             # Page routes
│   ├── layouts/           # Layout components
│   ├── components/        # Vue components
│   ├── stores/            # Pinia stores
│   ├── composables/       # Composable functions
│   ├── assets/            # Static assets
│   ├── nuxt.config.ts     # Nuxt configuration
│   ├── package.json
│   └── Dockerfile
└── docker-compose.yml     # Docker Compose configuration
```

## Prerequisites

- Docker and Docker Compose
- Git

## Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/grokathon.git
cd grokathon
```

### 2. Set up environment variables

```bash
cp .env.example .env
```

The `.env.example` file works for both development and production:
- **Development:** Default values work out of the box!
- **Production:** Update `DEBUG=False`, `SECRET_KEY`, passwords, and domain URLs

See [ENVIRONMENT.md](ENVIRONMENT.md) for detailed configuration guide.

**Important:** Never commit your `.env` file to version control!

### 3. Start with Docker Compose

```bash
# Development
docker-compose up --build

# Production  
docker-compose -f docker-compose.prod.yml up --build -d
```

This will start three services:
- **PostgreSQL** database on port 5432
- **Django backend** on http://localhost:8000
- **Nuxt frontend** on http://localhost:3000

### 4. Run database migrations

```bash
docker-compose exec backend python manage.py migrate
```

### 5. Create a superuser (optional)

```bash
docker-compose exec backend python manage.py createsuperuser
```

### 6. Access the application

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000/api
- Django Admin: http://localhost:8000/admin

## Development Without Docker

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables (if not done already in root)
cd .. && cp .env.example .env && cd backend

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start development server
python manage.py runserver
```

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Make sure .env is set up in the root directory

# Start development server
npm run dev
```

## Environment Variables

This project uses a single `.env.example` file that works for both development and production.

**Quick setup:**
```bash
cp .env.example .env
```

The `.env.example` file contains inline comments explaining which values to use for development vs production:
- **Development:** Default values work out of the box
- **Production:** Update `DEBUG`, `SECRET_KEY`, passwords, and domain URLs

**Critical for production:**
- `DEBUG=False`
- `SECRET_KEY` - Generate with: `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`
- `ALLOWED_HOSTS` - Your domain name(s)
- `DB_PASSWORD` - Strong password
- `CORS_ALLOWED_ORIGINS` - Your frontend URL(s)
- `NUXT_PUBLIC_API_BASE` - Your backend API URL

**For detailed environment configuration, see [ENVIRONMENT.md](ENVIRONMENT.md)**

### Required Environment Variables

| Variable | Description | Dev Example | Prod Example |
|----------|-------------|-------------|--------------|
| `DEBUG` | Django debug mode | `True` | `False` |
| `SECRET_KEY` | Django secret key | Default OK | Generate strong key |
| `ALLOWED_HOSTS` | Allowed hostnames | `*` | `yourdomain.com` |
| `DB_NAME` | Database name | `rapid_django_vue` | `rapid_django_vue` |
| `DB_USER` | Database user | `postgres` | `postgres` |
| `DB_PASSWORD` | Database password | `postgres` | Strong password |
| `DB_HOST` | Database host | `db` | `db` |
| `DB_PORT` | Database port | `5432` | `5432` |
| `CORS_ALLOWED_ORIGINS` | Frontend URLs | `http://localhost:3000` | `https://yourdomain.com` |
| `NUXT_PUBLIC_API_BASE` | Backend API URL | `http://localhost:8000/api` | `https://yourdomain.com/api` |

## API Endpoints

### Authentication

- `POST /api/auth/register/` - Register a new user
- `POST /api/auth/login/` - Login and receive JWT tokens
- `POST /api/auth/token/refresh/` - Refresh access token
- `GET /api/auth/user/` - Get current user details (requires authentication)

### Example Request - Register

```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "securepassword123",
    "password2": "securepassword123",
    "first_name": "Test",
    "last_name": "User"
  }'
```

### Example Request - Login

```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "securepassword123"
  }'
```

## Environment Variables

### Backend (.env)

```env
DEBUG=True
SECRET_KEY=your-secret-key
DB_NAME=rapid_django_vue
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
ALLOWED_HOSTS=*
CORS_ALLOWED_ORIGINS=http://localhost:3000
```

### Frontend (.env)

```env
NUXT_PUBLIC_API_BASE=http://localhost:8000/api
```

## Production Deployment

### Security Checklist

1. **Change SECRET_KEY** - Generate a new secret key for Django
2. **Set DEBUG=False** - Disable debug mode in production
3. **Configure ALLOWED_HOSTS** - Set specific domain names
4. **Update CORS settings** - Restrict CORS to your frontend domain
5. **Use environment variables** - Never commit sensitive data to Git
6. **Enable HTTPS** - Use SSL/TLS certificates
7. **Set strong database passwords**
8. **Configure static file serving** - Use WhiteNoise or CDN

### Docker Production Build

```bash
docker-compose -f docker-compose.prod.yml up --build -d
```

## Technology Stack

### Backend
- Python 3.11
- Django 4.2
- Django REST Framework 3.14
- djangorestframework-simplejwt 5.3
- PostgreSQL 15
- django-cors-headers 4.3

### Frontend
- Node.js 18
- Nuxt 3.8
- Vue 3.3
- Pinia 2.1
- TypeScript

## Common Commands

### Docker

```bash
# Start services
docker-compose up

# Stop services
docker-compose down

# Rebuild services
docker-compose up --build

# View logs
docker-compose logs -f

# Execute command in backend container
docker-compose exec backend python manage.py <command>

# Execute command in frontend container
docker-compose exec frontend npm run <command>
```

### Django

```bash
# Make migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic

# Run tests
python manage.py test
```

### Nuxt

```bash
# Install dependencies
npm install

# Development server
npm run dev

# Build for production
npm run build

# Generate static site
npm run generate

# Preview production build
npm run preview
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues and questions:
- Open an issue on GitHub
- Check existing issues for solutions

## Author

**Thomas Slabbers**
- 𝕏: [@thomasslabbers](https://x.com/thomasslabbers)
- GitHub: [@thomasslabbers](https://github.com/thomasslabbers)

## Acknowledgments

- Django REST Framework documentation
- Nuxt documentation
- Vue.js documentation
- Docker documentation
- Community contributors

---


