# Environment Configuration Guide

This document explains how to configure environment variables for Rapid Django Nuxt.

## Quick Start

### 1. Create your `.env` file

```bash
cp .env.example .env
```

### 2. Update values based on your environment

The `.env.example` file contains inline comments explaining what values to use for development vs production.

**For local development:** The default values work out of the box!

**For production:** Update these critical values:
- `DEBUG=False`
- `SECRET_KEY=<generate-a-strong-key>`
- `ALLOWED_HOSTS=yourdomain.com`
- `DB_PASSWORD=<strong-password>`
- `CORS_ALLOWED_ORIGINS=https://yourdomain.com`
- `NUXT_PUBLIC_API_BASE=https://yourdomain.com/api`

### 3. Start your application

```bash
# Development
docker-compose up --build

# Production
docker-compose -f docker-compose.prod.yml up -d
```

## Environment Variables Reference

| Variable | Required | Description | Dev Example | Prod Example |
|----------|----------|-------------|-------------|--------------|
| `DEBUG` | Yes | Enable debug mode | `True` | `False` |
| `SECRET_KEY` | Yes | Django secret key | Default is OK | Generate strong key |
| `ALLOWED_HOSTS` | Yes | Allowed hostnames | `*` or `localhost` | `yourdomain.com` |
| `DB_NAME` | Yes | Database name | `rapid_django_vue` | `rapid_django_vue` |
| `DB_USER` | Yes | Database user | `postgres` | `postgres` |
| `DB_PASSWORD` | Yes | Database password | `postgres` | Strong password |
| `DB_HOST` | Yes | Database host | `db` | `db` (Docker) |
| `DB_PORT` | Yes | Database port | `5432` | `5432` |
| `CORS_ALLOWED_ORIGINS` | Yes | Frontend URLs | `http://localhost:3000` | `https://yourdomain.com` |
| `NUXT_PUBLIC_API_BASE` | Yes | Backend API URL | `http://localhost:8000/api` | `https://yourdomain.com/api` |

## Generating a Secure SECRET_KEY

For production, generate a strong secret key:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copy the output and paste it into your `.env` file.

## Security Best Practices

### DO:

1. Generate a strong `SECRET_KEY` for production
2. Set `DEBUG=False` in production
3. Use strong database passwords (20+ characters)
4. Specify exact domains in `ALLOWED_HOSTS` (never use `*` in production)
5. Use HTTPS URLs in production
6. Keep your `.env` file secret - it's in `.gitignore`

### DON'T:

1. Never commit `.env` files to version control
2. Never use development settings in production
3. Never share your `SECRET_KEY` publicly
4. Never use `DEBUG=True` in production
5. Never use weak passwords in production

## Common Issues

### "SECRET_KEY not found" Error

**Solution:** Make sure you have a `.env` file:
```bash
cp .env.example .env
```

### Database Connection Failed

**Solution:**
1. Check database credentials in `.env`
2. Ensure PostgreSQL is running: `docker-compose ps`
3. Wait a few seconds for database to initialize

### CORS Errors in Browser

**Solution:**
1. Verify `CORS_ALLOWED_ORIGINS` matches your frontend URL
2. Ensure both frontend and backend are running
3. Check for typos (include `http://` or `https://`)

## Development vs Production

The same `.env.example` file works for both environments. The inline comments guide you on which values to use.

### Development Setup (Works out of the box)
```bash
cp .env.example .env
docker-compose up --build
```

### Production Setup (Update values first)
```bash
cp .env.example .env
nano .env  # Update: DEBUG, SECRET_KEY, passwords, domains
docker-compose -f docker-compose.prod.yml up -d
```

## Example: Deploying to Hetzner VPS

```bash
# 1. SSH into your server
ssh user@your-server-ip

# 2. Clone your repository
git clone https://github.com/yourusername/grokathon.git
cd grokathon

# 3. Set up environment
cp .env.example .env

# 4. Generate secret key
python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# 5. Edit .env with production values
nano .env
# Update:
# - DEBUG=False
# - SECRET_KEY=<paste-generated-key>
# - ALLOWED_HOSTS=yourdomain.com
# - DB_PASSWORD=<strong-password>
# - CORS_ALLOWED_ORIGINS=https://yourdomain.com
# - NUXT_PUBLIC_API_BASE=https://yourdomain.com/api

# 6. Start production services
docker-compose -f docker-compose.prod.yml up -d

# 7. Run migrations
docker-compose -f docker-compose.prod.yml exec backend python manage.py migrate

# 8. Create superuser
docker-compose -f docker-compose.prod.yml exec backend python manage.py createsuperuser
```

## Need Help?

- Check the [README.md](README.md) for more details
- Review the [DEPLOYMENT.md](DEPLOYMENT.md) guide
- Open an issue on GitHub

---

**Remember:** Always keep your `.env` file secure and never commit it to version control!
