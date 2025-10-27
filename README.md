# DIRI Planner

A Django-based application management system with hierarchical organization structures, attributes, and full CRUD functionality.

## Features

- **Application Management**: Full CRUD operations for applications with hierarchical relationships
- **Organisation Structure**: Tree-based organization hierarchy with contact information
- **Attributes System**: Flexible attribute system with multiple data types
- **Clean UI**: Simple, responsive interface with no external dependencies
- **Comprehensive Testing**: 33 automated tests covering all functionality

## Technology Stack

- **Framework**: Django 5.2.7
- **Database**: PostgreSQL
- **Package Manager**: uv (Python package manager)
- **CRUD Framework**: Neapolitan (lightweight Django CRUD)
- **Tree Structure**: django-fast-treenode
- **Admin Enhancements**: django-dynamic-admin-forms

## Quick Start

### 1. Prerequisites

- Python 3.12+
- PostgreSQL
- uv package manager

### 2. Setup

```bash
# Clone the repository
git clone <repository-url>
cd diri-planner-1.5

# Install dependencies using uv
uv sync

# Set up environment variables
cp .env.example .env
# Edit .env with your database credentials

# Run migrations
uv run python manage.py migrate

# Create a superuser (optional)
uv run python manage.py createsuperuser
```

### 3. Load Fixtures

Choose one of the available fixtures:

```bash
# Load test data (neutral fixtures for testing)
uv run python manage.py loaddata test_data

# OR load current data (production-like data)
uv run python manage.py loaddata current_data
```

### 4. Run Development Server

```bash
uv run python manage.py runserver 8000
```

Visit http://localhost:8000 to access the application.

### 5. Run Tests

```bash
# Run all tests
uv run python manage.py test core.tests

# Run tests with verbose output
uv run python manage.py test core.tests --verbosity=2

# Run specific test file
uv run python manage.py test core.tests.test_application_model

# Run specific test class
uv run python manage.py test core.tests.test_application_model.ApplicationModelTest
```

## Project Structure

```
diri-planner-1.5/
├── config/                 # Django project settings
├── core/                   # Main application
│   ├── admin/             # Admin configurations
│   ├── fixtures/          # Data fixtures
│   │   ├── test_data.json       # Test fixtures
│   │   └── current_data.json    # Production data dump
│   ├── migrations/        # Database migrations
│   ├── models/            # Data models
│   ├── static/            # Static files (CSS, JS)
│   │   └── css/
│   │       └── application.css  # Main stylesheet
│   ├── templates/         # HTML templates
│   ├── tests/             # Test suite (33 tests)
│   │   ├── test_application_model.py
│   │   ├── test_attribute_model.py
│   │   ├── test_organisation_model.py
│   │   ├── test_application_views.py
│   │   ├── test_application_integration.py
│   │   └── test_home_redirect.py
│   └── views/             # View logic
├── docs/                  # Documentation
├── pyproject.toml         # Project dependencies
└── README.md             # This file
```

## Available URLs

- `/` - Redirects to application list
- `/application/` - List all applications
- `/application/new/` - Create new application
- `/application/<uuid>/` - View application details
- `/application/<uuid>/edit/` - Edit application
- `/application/<uuid>/delete/` - Delete application
- `/admin/` - Django admin interface

## Development

### Creating Database Dumps

```bash
# Dump current database to fixtures
uv run python manage.py dumpdata core --indent 2 --output core/fixtures/backup.json
```

### Resetting Database

```bash
# Reset database (WARNING: deletes all data)
uv run python reset_database.py

# Re-run migrations
uv run python manage.py migrate

# Load fixtures
uv run python manage.py loaddata test_data
```

## Development Tools

### Install Development Dependencies

```bash
# Install development tools
uv pip install --dev
```

### Code Quality Tools

#### Ruff (Linting)
```bash
# Check code
uv run ruff check .

# Fix auto-fixable issues
uv run ruff check . --fix
```

#### Black (Formatting)
```bash
# Check formatting
uv run black --check .

# Format code
uv run black .
```

#### isort (Import Sorting)
```bash
# Check imports
uv run isort --check-only .

# Sort imports
uv run isort .
```

#### Run All Quality Checks
```bash
# Create a script or run them all
uv run ruff check . && uv run black --check . && uv run isort --check-only .
```

### Security Scanning

```bash
# Check for vulnerabilities in dependencies
uv run safety check

# Security audit of code
uv run bandit -r . -f json -o bandit-report.json
```

### Code Coverage

```bash
# Run tests with coverage
uv run coverage run --source='.' manage.py test core.tests

# Generate coverage report
uv run coverage report

# Generate HTML coverage report
uv run coverage html
# Open htmlcov/index.html in browser
```

### Pre-commit Checks

Create a script to run before committing:

```bash
#!/bin/bash
# pre-commit-check.sh

echo "Running code quality checks..."
uv run ruff check . || exit 1
uv run black --check . || exit 1
uv run isort --check-only . || exit 1
uv run python manage.py test core.tests || exit 1
echo "All checks passed!"
```

## Testing

The project includes comprehensive test coverage:

- **Model Tests**: 18 tests covering Application, Attribute, and Organisation models
- **View Tests**: 12 tests covering all CRUD operations
- **Integration Tests**: 3 end-to-end workflow tests
- **Other Tests**: 1 test for URL routing

All tests use the `test_data.json` fixture for consistent, isolated testing.

## Production Deployment with Docker

The application includes Docker configuration for production deployment with Nginx reverse proxy.

### Prerequisites

- Docker
- Docker Compose

### Build and Deploy

```bash
# 1. Create production environment file
cp .env.prod.example .env.prod
# Edit .env.prod with your production credentials

# 2. Build and start services
docker-compose -f docker-compose.prod.yaml up -d --build

# 3. Check service health
docker-compose -f docker-compose.prod.yaml ps

# 4. View logs
docker-compose -f docker-compose.prod.yaml logs -f

# 5. Run migrations (first time only)
docker-compose -f docker-compose.prod.yaml exec web python manage.py migrate

# 6. Create superuser (first time only)
docker-compose -f docker-compose.prod.yaml exec web python manage.py createsuperuser

# 7. Load fixtures (optional)
docker-compose -f docker-compose.prod.yaml exec web python manage.py loaddata test_data
```

### Services

The production stack includes:

- **web**: Django application running with Gunicorn (4 workers)
- **db**: PostgreSQL 15 database
- **nginx**: Nginx reverse proxy serving static files and proxying to Django

### Accessing the Application

Once deployed, the application is available at:
- **Application**: http://localhost
- **Admin**: http://localhost/admin/
- **Health Check**: http://localhost/health/

### Stopping Services

```bash
# Stop services
docker-compose -f docker-compose.prod.yaml down

# Stop and remove volumes (WARNING: deletes all data)
docker-compose -f docker-compose.prod.yaml down -v
```

### Production Checklist

Before deploying to production:

1. ✅ Set `DEBUG=False` in `.env.prod`
2. ✅ Generate a strong `SECRET_KEY`
3. ✅ Set appropriate `ALLOWED_HOSTS`
4. ✅ Use strong database credentials
5. ✅ Configure SSL/TLS certificates in nginx
6. ✅ Set up backup strategy for database
7. ✅ Configure monitoring and logging
8. ✅ Review and harden security settings

## CI/CD Pipeline

The project includes comprehensive GitHub Actions workflows for continuous integration and deployment.

### Workflows

#### 1. CI - Tests and Linting (`.github/workflows/ci.yaml`)
Runs on every push and pull request to `main` and `develop` branches.

**Jobs:**
- **Test**: Runs all 33 tests with PostgreSQL service container
- **Lint**: Code quality checks with Ruff, Black, and isort
- **Security**: Security scans with Safety and Bandit
- **Coverage**: Generates coverage reports and uploads to Codecov

#### 2. CD - Build and Deploy (`.github/workflows/cd.yaml`)
Runs on pushes to `main` branch and version tags.

**Jobs:**
- **Build**: Builds and pushes Docker image to GitHub Container Registry
- **Deploy Staging**: Automatically deploys to staging on main branch
- **Deploy Production**: Deploys to production on version tags (v*)

#### 3. Dependency Updates (`.github/workflows/dependency-update.yaml`)
Runs weekly to check for outdated dependencies.

**Features:**
- Checks for package updates
- Creates issues for review
- Runs every Monday at 9 AM UTC

### Setting Up CI/CD

1. **Enable GitHub Actions** in your repository settings

2. **Configure Secrets** (Settings → Secrets and variables → Actions):
   ```
   No secrets required for basic CI
   Add deployment secrets as needed:
   - DEPLOY_SSH_KEY (for SSH deployments)
   - REGISTRY_USERNAME (if using external registry)
   - REGISTRY_PASSWORD (if using external registry)
   ```

3. **Configure Environments** (Settings → Environments):
   - Create `staging` environment
   - Create `production` environment with protection rules

4. **Enable Branch Protection** (Settings → Branches):
   - Require pull request reviews
   - Require status checks to pass before merging
   - Require CI workflow to pass

### Triggering Deployments

```bash
# Deploy to staging (push to main)
git push origin main

# Deploy to production (create version tag)
git tag v1.0.0
git push origin v1.0.0

# Manual deployment
# Go to Actions → CD - Build and Deploy → Run workflow
```

### Monitoring Builds

View build status and logs:
- **Actions tab** in GitHub repository
- **Commit status checks** on pull requests
- **Email notifications** for failed builds

## Database Configuration

Default PostgreSQL settings (configure in `.env`):

```env
POSTGRES_DB=diri_planner
POSTGRES_USER=diri_user
POSTGRES_PASSWORD=diri_password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```

## Contributing

1. Write tests for new features
2. Ensure all tests pass before committing
3. Follow Django best practices
4. Update documentation as needed

## License

[Your License Here]