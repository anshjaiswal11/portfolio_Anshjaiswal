# 🚀 Django Portfolio Site

A full-stack portfolio website built with Django, PostgreSQL, Docker, and GitHub Actions CI/CD. Demonstrates every core full-stack concept including REST APIs, authentication, email, admin panel, and containerized deployment.

[![CI/CD Pipeline](https://github.com/yourusername/portfolio-site/actions/workflows/ci.yml/badge.svg)](https://github.com/yourusername/portfolio-site/actions)
[![Python](https://img.shields.io/badge/Python-3.11-blue)](https://python.org)
[![Django](https://img.shields.io/badge/Django-4.2-green)](https://djangoproject.com)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue)](https://docker.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## ✨ Features

### 🌐 Public Portfolio
- **Home Page** — Hero section, skills, featured projects, call-to-action
- **About Page** — Profile, bio, skills, education, experience, resume download
- **Projects Page** — Filterable grid with slug-based URLs
- **Project Detail** — Full project page with tech stack, links, related projects
- **Contact Page** — Contact form with email notifications (admin + confirmation)

### 🔐 Authentication & Authorization
- Signup / Login / Logout with password validation
- Protected dashboard (login required)
- Admin-only project CRUD operations
- Token-based API authentication (DRF)

### 🗄️ Database & Models
- **PostgreSQL** with Django ORM
- `Profile` model — bio, skills, resume, social links
- `Project` model — title, slug, description, tech stack, GitHub/demo links
- `ContactMessage` model — name, email, message, read status, timestamp
- Auto-slug generation, migrations, Django Admin with search/filter

### 📡 REST API (Django REST Framework)
| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/api/projects/` | Public | List all projects |
| POST | `/api/projects/` | Admin Token | Create project |
| GET | `/api/projects/{slug}/` | Public | Get project detail |
| PUT/PATCH | `/api/projects/{slug}/` | Admin Token | Update project |
| DELETE | `/api/projects/{slug}/` | Admin Token | Delete project |
| GET | `/api/projects/featured/` | Public | Featured projects |
| POST | `/api/contact/` | Public | Submit contact message |
| GET | `/api/profile/` | Public | Get portfolio profile |
| POST | `/api/auth/login/` | Public | Get auth token |
| POST | `/api/auth/logout/` | Token | Invalidate token |
| GET | `/api/auth/profile/` | Token | Get current user profile |

### 📧 Email Service
- Contact form sends email notification to admin
- Sends confirmation email to the user
- SMTP via Gmail or SendGrid
- Development: console backend (prints to terminal)

### 🐳 Docker & DevOps
- Multi-stage `Dockerfile` with non-root user
- `docker-compose.yml` with Django + PostgreSQL + Nginx
- Health checks and proper startup ordering
- Environment variables via `.env`

### ⚙️ CI/CD (GitHub Actions)
- Code quality (flake8, black, isort)
- Automated tests with PostgreSQL service
- Coverage reporting (Codecov)
- Docker image build & push to GHCR

---

## 📁 Project Structure

```
portfolio_site/
├── accounts_app/           # Authentication, profiles, dashboard
│   ├── models.py           # Profile model
│   ├── views.py            # signup, login, logout, dashboard
│   ├── forms.py            # SignupForm, LoginForm, ProfileForm
│   ├── signals.py          # Auto-create profile on user creation
│   └── admin.py
├── projects_app/           # Portfolio projects
│   ├── models.py           # Project model with auto-slug
│   ├── views.py            # CRUD views
│   ├── forms.py
│   ├── admin.py            # Custom admin with search/filter
│   └── management/commands/wait_for_db.py
├── contact_app/            # Contact form & messages
│   ├── models.py           # ContactMessage model
│   ├── views.py            # Contact form with email
│   └── admin.py
├── api_app/                # Django REST Framework
│   ├── serializers.py      # ModelSerializer with validation
│   ├── views.py            # API views, login endpoint
│   └── urls.py
├── portfolio_site/         # Django project settings
│   ├── settings.py
│   ├── urls.py
│   ├── jinja2.py           # Jinja2 environment
│   └── wsgi.py
├── templates/              # Jinja2 HTML templates
│   ├── base.html           # Base with navbar, footer, flash messages
│   ├── home.html
│   ├── about.html
│   ├── projects/
│   │   ├── list.html
│   │   ├── detail.html
│   │   ├── form.html
│   │   └── confirm_delete.html
│   ├── contact/contact.html
│   └── accounts/
│       ├── login.html
│       ├── signup.html
│       ├── dashboard.html
│       └── profile_edit.html
├── static/                 # Static files (CSS, JS, images)
├── nginx/nginx.conf        # Nginx reverse proxy config
├── .github/workflows/ci.yml # GitHub Actions CI/CD
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
├── pytest.ini
└── tests.py                # Comprehensive test suite
```

---

## 🚀 Quick Start (Local Development)

### Prerequisites
- Python 3.11+
- PostgreSQL 14+
- pip

### 1. Clone & Setup

```bash
git clone https://github.com/yourusername/portfolio-site.git
cd portfolio-site

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env with your database credentials and settings
```

Key variables in `.env`:
```env
SECRET_KEY=your-secret-key-here
DEBUG=True
DB_NAME=portfolio_db
DB_USER=your_pg_user
DB_PASSWORD=your_pg_password
DB_HOST=localhost
```

### 3. Database Setup

```bash
# Create PostgreSQL database
psql -U postgres -c "CREATE DATABASE portfolio_db;"
psql -U postgres -c "CREATE USER portfolio_user WITH PASSWORD 'portfolio_pass';"
psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE portfolio_db TO portfolio_user;"

# Run migrations
python manage.py migrate

# Create superuser (admin)
python manage.py createsuperuser

# Optional: Load sample data
# python manage.py loaddata sample_data.json
```

### 4. Run Development Server

```bash
python manage.py runserver
```

Visit: http://localhost:8000

---

## 🐳 Docker Setup

### Using Docker Compose (Recommended)

```bash
# Copy environment file
cp .env.example .env
# Edit .env as needed

# Build and start all services (Django + PostgreSQL + Nginx)
docker-compose up --build

# In another terminal, create admin user
docker-compose exec web python manage.py createsuperuser

# Access the site
# http://localhost (via Nginx)
# http://localhost:8000 (direct Django)
```

### Docker Commands Reference

```bash
# Run in background
docker-compose up -d

# View logs
docker-compose logs -f web
docker-compose logs -f db

# Run migrations
docker-compose exec web python manage.py migrate

# Open Django shell
docker-compose exec web python manage.py shell

# Run tests inside container
docker-compose exec web python manage.py test

# Stop all services
docker-compose down

# Stop and remove volumes (fresh start)
docker-compose down -v
```

---

## 📡 API Documentation

### Authentication

**Get Token:**
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "yourpassword"}'
```

Response:
```json
{
  "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
  "user_id": 1,
  "username": "admin",
  "is_staff": true
}
```

**Use Token:**
```bash
curl -H "Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b" \
  http://localhost:8000/api/projects/
```

### Projects API Examples

```bash
# List all projects
curl http://localhost:8000/api/projects/

# Get project by slug
curl http://localhost:8000/api/projects/my-awesome-project/

# Create project (admin required)
curl -X POST http://localhost:8000/api/projects/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "New Project",
    "description": "Detailed description of the project.",
    "tech_stack": "Python, Django, PostgreSQL"
  }'

# Submit contact message
curl -X POST http://localhost:8000/api/contact/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "message": "Hello! I am interested in working with you."
  }'
```

---

## 📧 Email Configuration

### Gmail SMTP Setup
1. Enable 2-Factor Authentication on your Google account
2. Go to Google Account → Security → App Passwords
3. Generate an app password for "Mail"
4. Update `.env`:
```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your@gmail.com
EMAIL_HOST_PASSWORD=your-16-char-app-password
ADMIN_EMAIL=admin@yoursite.com
```

### SendGrid Setup
```env
EMAIL_HOST=smtp.sendgrid.net
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=apikey
EMAIL_HOST_PASSWORD=your-sendgrid-api-key
```

---

## 🧪 Running Tests

```bash
# Run all tests
pytest

# With coverage report
coverage run -m pytest
coverage report
coverage html  # Opens in browser: htmlcov/index.html

# Run specific test class
pytest tests.py::ProjectModelTest -v

# Run with Django test runner
python manage.py test
```

---

## 🔒 Django Admin Panel

Access: http://localhost:8000/admin/

Features:
- **Projects** — Create/edit/delete with slug auto-generation, search by title/tech, filter by featured/date
- **Contact Messages** — View all messages, mark as read/unread, bulk actions
- **Profiles** — Manage user profiles

---

## ⚙️ CI/CD Pipeline (GitHub Actions)

The `.github/workflows/ci.yml` pipeline runs on every push/PR:

```
Push/PR → Lint (flake8/black) → Tests (PostgreSQL) → Docker Build → Push to GHCR
```

### Setup GitHub Secrets
For the push-to-registry job, no additional secrets needed (uses `GITHUB_TOKEN`).

For deployment secrets, add in GitHub → Settings → Secrets:
- `DJANGO_SECRET_KEY` — Production secret key
- `DB_PASSWORD` — Production database password

---

## 🌐 Deployment

### Manual VPS Deployment

```bash
# On your server
git clone https://github.com/yourusername/portfolio-site.git
cd portfolio-site
cp .env.example .env
# Edit .env with production values (DEBUG=False, secure SECRET_KEY, etc.)

docker-compose up -d --build
docker-compose exec web python manage.py createsuperuser
```

### Environment for Production
```env
DEBUG=False
SECRET_KEY=very-long-random-secret-key-at-least-50-chars
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
# ... database, email settings
```

---

## 📋 Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | Python 3.11, Django 4.2 |
| API | Django REST Framework 3.15 |
| Database | PostgreSQL 15 |
| Frontend | Jinja2 Templates, Tailwind CSS, JavaScript |
| Auth | Django Auth + DRF Token Auth |
| Email | Django Email + SMTP (Gmail/SendGrid) |
| Containerization | Docker, Docker Compose |
| Web Server | Gunicorn + Nginx |
| CI/CD | GitHub Actions |
| Testing | pytest, coverage |

---

## 📄 License

MIT License — feel free to use this as a template for your own portfolio!

---

*Built with Django 🐍 | Containerized with Docker 🐳 | Deployed with GitHub Actions ⚙️*
