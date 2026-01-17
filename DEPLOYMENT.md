# Deployment Guide

This guide covers deploying Rapid Django Vue to production.

## Pre-Deployment Checklist

### Security
- [ ] Change Django `SECRET_KEY` to a strong, random value
- [ ] Set `DEBUG=False` in Django settings
- [ ] Configure `ALLOWED_HOSTS` with your domain
- [ ] Set strong database password
- [ ] Update CORS settings to only allow your frontend domain
- [ ] Enable HTTPS/SSL
- [ ] Review and update all security settings

### Configuration
- [ ] Set up production environment variables
- [ ] Configure static file serving
- [ ] Set up database backups
- [ ] Configure logging
- [ ] Set up monitoring (optional)

## Production Environment Variables

Create a `.env` file based on `.env.prod.example`:

```env
DEBUG=False
SECRET_KEY=<generate-a-strong-secret-key>
ALLOWED_HOSTS=yourdomain.com
DB_NAME=rapid_django_vue
DB_USER=prod_user
DB_PASSWORD=<strong-password>
DB_HOST=db
DB_PORT=5432
CORS_ALLOWED_ORIGINS=https://yourdomain.com
VUE_APP_API_URL=https://yourdomain.com/api
```

## Generate Secret Key

```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

## Deployment Options

### Option 1: Docker Compose (Simple)

Best for: Small to medium projects, VPS hosting

1. **Clone the repository on your server:**
```bash
git clone https://github.com/yourusername/grokathon.git
cd grokathon
```

2. **Set up environment variables:**
```bash
cp .env.prod.example .env
# Edit .env with your production values
nano .env
```

3. **Build and start services:**
```bash
docker-compose -f docker-compose.prod.yml up --build -d
```

4. **Run migrations:**
```bash
docker-compose -f docker-compose.prod.yml exec backend python manage.py migrate
```

5. **Create superuser:**
```bash
docker-compose -f docker-compose.prod.yml exec backend python manage.py createsuperuser
```

6. **Collect static files:**
```bash
docker-compose -f docker-compose.prod.yml exec backend python manage.py collectstatic --noinput
```

### Option 2: Cloud Platforms

#### AWS (Elastic Beanstalk / ECS)
- Use Docker Compose or separate containers
- Configure RDS for PostgreSQL
- Use S3 for static files
- CloudFront for CDN

#### Google Cloud Platform
- Cloud Run for containers
- Cloud SQL for PostgreSQL
- Cloud Storage for static files

#### DigitalOcean
- App Platform with Docker support
- Managed PostgreSQL database
- Spaces for static files

#### Heroku
- Use Heroku Postgres addon
- Deploy backend and frontend separately
- Configure buildpacks

### Option 3: Kubernetes

For large-scale deployments:
- Create Kubernetes manifests
- Use managed database service
- Configure ingress for routing
- Set up auto-scaling

## Database Setup

### PostgreSQL Production Settings

```sql
CREATE DATABASE rapid_django_vue;
CREATE USER prod_user WITH PASSWORD 'strong_password';
ALTER ROLE prod_user SET client_encoding TO 'utf8';
ALTER ROLE prod_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE prod_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE rapid_django_vue TO prod_user;
```

### Backups

Set up automated backups:
```bash
# PostgreSQL backup
pg_dump -U prod_user rapid_django_vue > backup_$(date +%Y%m%d_%H%M%S).sql

# Restore
psql -U prod_user rapid_django_vue < backup_file.sql
```

## Static Files

### Option 1: WhiteNoise (Recommended for simple deployments)

Already configured in the project. No additional setup needed.

### Option 2: CDN (Recommended for production)

1. **AWS S3 + CloudFront:**
```python
# settings.py
AWS_ACCESS_KEY_ID = 'your-key'
AWS_SECRET_ACCESS_KEY = 'your-secret'
AWS_STORAGE_BUCKET_NAME = 'your-bucket'
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/static/'
```

## SSL/HTTPS Setup

### Using Let's Encrypt (Certbot)

```bash
# Install certbot
sudo apt-get update
sudo apt-get install certbot python3-certbot-nginx

# Get certificate
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Auto-renewal
sudo certbot renew --dry-run
```

### Using Cloudflare

1. Point your domain to Cloudflare nameservers
2. Enable SSL/TLS in Cloudflare dashboard
3. Set SSL mode to "Full" or "Full (strict)"

## Monitoring and Logging

### Application Monitoring

**Sentry for Error Tracking:**
```bash
pip install sentry-sdk
```

```python
# settings.py
import sentry_sdk

sentry_sdk.init(
    dsn="your-sentry-dsn",
    traces_sample_rate=1.0,
)
```

### Server Monitoring

- **Uptime monitoring**: UptimeRobot, Pingdom
- **Performance**: New Relic, DataDog
- **Logs**: Papertrail, Loggly

## Performance Optimization

### Backend
- Enable Django caching (Redis/Memcached)
- Use database connection pooling
- Optimize database queries
- Enable gzip compression

### Frontend
- Enable browser caching
- Minimize and bundle assets
- Use CDN for static files
- Implement lazy loading

### Database
- Add database indexes
- Optimize queries
- Enable query caching
- Regular VACUUM operations (PostgreSQL)

## Scaling

### Horizontal Scaling
- Use load balancer (Nginx, AWS ELB)
- Deploy multiple backend instances
- Use managed database service
- Shared session storage (Redis)

### Vertical Scaling
- Increase server resources
- Optimize database performance
- Use caching aggressively

## Rollback Strategy

```bash
# Tag your releases
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0

# Rollback to previous version
git checkout v1.0.0
docker-compose -f docker-compose.prod.yml up --build -d
```

## Health Checks

Add health check endpoints:

```python
# urls.py
from django.http import JsonResponse

def health_check(request):
    return JsonResponse({"status": "ok"})

urlpatterns = [
    path('health/', health_check),
    # ... other urls
]
```

## Continuous Deployment

### GitHub Actions Example

```yaml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to server
        run: |
          ssh user@server 'cd /app && git pull && docker-compose -f docker-compose.prod.yml up --build -d'
```

## Troubleshooting

### Common Issues

1. **Static files not loading**
   - Run `collectstatic`
   - Check STATIC_URL and STATIC_ROOT

2. **Database connection errors**
   - Verify database credentials
   - Check network connectivity
   - Ensure database service is running

3. **CORS errors**
   - Update CORS_ALLOWED_ORIGINS
   - Check frontend API URL

4. **502 Bad Gateway**
   - Backend service not running
   - Check backend logs
   - Verify network configuration

## Support

For deployment issues:
- Check logs: `docker-compose logs`
- Review Django logs
- Check Nginx error logs

---

**Remember**: Always test your deployment in a staging environment first!

