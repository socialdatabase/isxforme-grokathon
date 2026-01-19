# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Grokathon application - a Django REST Framework backend with a Nuxt 3 frontend that provides expert insights and analysis on various topics using data from X (Twitter) and xAI's Grok API. The application allows users to explore expert perspectives, generate debates, create podcasts/newspapers, and convert content to speech using xAI's voice models.

## Development Commands

### Docker (Recommended Development Environment)

```bash
# Start all services (frontend, backend, database)
docker-compose up --build

# Stop all services
docker-compose down

# View logs
docker-compose logs -f

# Run backend commands in container
docker-compose exec backend python manage.py <command>

# Run frontend commands in container
docker-compose exec frontend npm run <command>
```

### Backend (Django)

```bash
# Run migrations
docker-compose exec backend python manage.py migrate

# Create migrations after model changes
docker-compose exec backend python manage.py makemigrations

# Create superuser for admin access
docker-compose exec backend python manage.py createsuperuser

# Run tests
docker-compose exec backend python manage.py test

# Django shell for debugging
docker-compose exec backend python manage.py shell

# Collect static files (production)
docker-compose exec backend python manage.py collectstatic
```

### Frontend (Nuxt 3)

```bash
# Development server (runs automatically in docker-compose)
npm run dev

# Build for production
npm run build

# Generate static site
npm run generate

# Preview production build
npm run preview
```

### Makefile Commands

The project includes a Makefile with shortcuts:

```bash
make build          # Build Docker containers
make up             # Start services
make down           # Stop services
make restart        # Restart services
make logs           # View logs
make migrate        # Run Django migrations
make makemigrations # Create Django migrations
make createsuperuser # Create Django superuser
make shell          # Open Django shell
make test           # Run tests
make clean          # Remove containers and volumes
```

## Architecture Overview

### Backend Architecture

**Django Project Structure:**
- `config/` - Django settings and URL configuration
- `users/` - JWT authentication app (register, login, token refresh)
- `api/` - Main Grokathon API app

**Key Backend Modules (api/):**

- `views.py` - Main `GrokathonViewSet` with all API endpoints
  - **Social Database API**: `fetch-ids`, `fetch-accounts`, `fetch-posts`, `fetch-topics`
  - **Grok AI Streaming**: `stream-expert-perspective`, `stream-expert-overview`, `stream-followup`, `stream-debate-response`
  - **xAI Voice API**: `xai-text-to-speech`, `xai-speech-to-text`, `xai-voices`
  - **Content Generation**: `generate-newspaper`, `generate-podcast-script`

- `groksignal.py` - Grok AI integration for expert analysis, debates, and bio generation
- `timeline.py` - Social Database API integration for fetching X (Twitter) data
- `newspaper.py` - Newspaper article generation from social media posts
- `voicethomas.py` / `tts.py` - xAI text-to-speech/speech-to-text integration
- `image.py` - xAI image-to-video generation
- `core.py` - Custom filters and throttling (`QueryFilter`, `BotThrottle`)
- `serializers.py` - DRF serializers for all endpoints

**Authentication:**
- JWT-based authentication using `djangorestframework-simplejwt`
- Grokathon API endpoints are **open** (no auth required, throttled instead)
- User endpoints require JWT tokens

**Throttling:**
- Custom `BotThrottle` class: 60 requests/min, then blocks for 1 hour
- Applied to all Grokathon endpoints to prevent bot flooding

### Frontend Architecture

**Nuxt 3 Structure:**
- `app/pages/` - Route pages (index.vue, result/index.vue)
- `app/components/` - Vue components (ResultOverview, ResultExpertDebate, ResultTimeline, etc.)
- `app/layouts/` - Layout templates (default.vue)
- `app/stores/` - Pinia state management (auth.ts)
- `app/composables/` - Reusable composables (useApi.ts for API calls)
- `app/assets/` - Static assets and CSS

**Key Frontend Patterns:**

- **SPA Mode**: `ssr: false` in nuxt.config.ts - client-side rendering only
- **API Integration**: `useApi` composable provides authenticated API calls with JWT token refresh
- **State Management**: Pinia stores for auth state
- **Styling**: Nuxt UI module (@nuxt/ui) for components

### API Integration

**Backend Base URL**: Configured via `NUXT_PUBLIC_API_BASE` environment variable (default: `http://localhost:8000/api`)

**Authentication Flow:**
1. User registers/logs in → receives JWT access + refresh tokens
2. Frontend stores tokens in auth store
3. `useApi` composable adds Bearer token to requests
4. On 401, automatically attempts token refresh
5. If refresh fails, logs out user

**Streaming Endpoints:**
- Several endpoints return `StreamingHttpResponse` for real-time data delivery
- Used for Grok AI responses (expert perspectives, debates, bios)
- Frontend must handle streaming text responses

### Environment Variables

**Critical Environment Variables:**

Backend (`.env` in root):
- `SECRET_KEY` - Django secret key
- `DEBUG` - Debug mode (True/False)
- `ALLOWED_HOSTS` - Comma-separated allowed hosts
- `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT` - PostgreSQL config
- `CORS_ALLOWED_ORIGINS` - Frontend URLs for CORS
- `SOCIAL_DATABASE_TOKEN` - API token for Social Database (X data)
- `X_BEARER_TOKEN` - X (Twitter) API bearer token
- `XAI_TOKEN` - xAI API token for Grok

Frontend:
- `NUXT_PUBLIC_API_BASE` - Backend API URL

### Database

- **PostgreSQL 15** used for production
- Default database name: `rapid_django_nuxt`
- Database runs on port 5432 in Docker
- Migrations managed through Django ORM

### External APIs

**Social Database API:**
- Used to fetch X (Twitter) user IDs, accounts, posts, topics, and rankings
- Token required: `SOCIAL_DATABASE_TOKEN`
- Base URL: `https://www.socialdatabase.org/api/ids/get`

**X API (Twitter):**
- Used to fetch account details by username
- Bearer token required: `X_BEARER_TOKEN`
- Endpoint: `https://api.twitter.com/2/users/by`

**xAI Grok API:**
- Used for AI-powered analysis, debates, content generation
- Token required: `XAI_TOKEN`
- Base URL: `https://api.x.ai/v1`
- Models used: `grok-4-1-fast-non-reasoning`, `grok-4-1-preview`

**xAI Voice API:**
- Text-to-speech and speech-to-text functionality
- Voices: ara, rex, sal, eve, una, leo
- Audio format: WAV, PCM linear16, 24kHz
- Integrated via `xai_sdk` and custom implementations

### Key Technical Considerations

**Async/Sync Bridge:**
- Grok AI functions are async generators (`async for`)
- Django views are sync - use `asyncio.new_event_loop()` to bridge
- Pattern used in streaming endpoints to convert async generators to sync

**CORS Configuration:**
- Development: `CORS_ALLOW_ALL_ORIGINS = True` when `DEBUG=True`
- Production: Specific origins from `CORS_ALLOWED_ORIGINS` environment variable
- `CORS_ALLOW_CREDENTIALS = True` for auth cookies

**CSRF Configuration:**
- `CSRF_TRUSTED_ORIGINS` configured for frontend URLs
- CSRF disabled for development (insecure cookies allowed)
- Grokathon endpoints use `@csrf_exempt` decorator

**JSON Response Formats:**
- Most endpoints return JSON via DRF serializers
- Streaming endpoints return plain text (streaming content)
- TTS endpoints return binary audio data (WAV format)

## Testing

**Backend Tests:**
- Standard Django tests in `api/tests.py` and `users/tests.py`
- Standalone test scripts in root: `test_groksignal.py`, `test_stream_endpoint.py`, etc.
- Run Django tests: `docker-compose exec backend python manage.py test`

**Test Function in views.py:**
- `test()` function in `api/views.py` provides integration testing
- Tests various Grokathon endpoints end-to-end
- Can be called from Django shell for manual testing

## Common Development Tasks

**Adding New API Endpoints:**
1. Add serializer class in `api/serializers.py`
2. Add action method to `GrokathonViewSet` in `api/views.py` with `@action` decorator
3. Specify URL path, methods, and query filters
4. URLs auto-registered via DRF router in `api/urls.py`

**Working with Grok AI:**
- Functions in `api/groksignal.py` handle Grok integration
- Use async generators for streaming responses
- Include proper error handling for API failures
- Model selection: fast non-reasoning for quick responses, preview for complex analysis

**Adding New Voice Features:**
- TTS/STT logic in `api/voicethomas.py` and `api/tts.py`
- Supports multiple voices - infer gender from names for appropriate voice selection
- Stream audio chunks for real-time playback or return complete WAV files

## Service URLs

When services are running:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000/api
- **Django Admin**: http://localhost:8000/admin
- **PostgreSQL**: localhost:5432

## Production Deployment

See `DEPLOYMENT.md` for detailed production deployment instructions.

Key production considerations:
- Set `DEBUG=False`
- Generate strong `SECRET_KEY`
- Configure specific `ALLOWED_HOSTS`
- Use strong database passwords
- Set up SSL/TLS certificates
- Configure proper CORS origins
- Use `docker-compose.prod.yml` for production builds
