# PostgreSQL Database Setup with Docker

This guide explains how to set up and use the PostgreSQL database for the diri-planner Django project using Docker Compose.

## Prerequisites

- Docker installed and running on your system
- Docker Compose installed
- Python 3.12 or higher
- UV package manager (or pip)

## Environment Variables Setup

This project uses a [`.env`](.env) file for local configuration and [`.env.example`](.env.example) as a template for version control.

### Step 0: Create Your Local .env File

Copy the example environment file to create your local configuration:

```bash
cp .env.example .env
```

Then edit [`.env`](.env) with your actual database credentials and settings:

```bash
# Django Settings
SECRET_KEY=your-unique-secret-key-generate-a-new-one
DEBUG=True

# Database Configuration
POSTGRES_DB=diri_planner
POSTGRES_USER=diri_user
POSTGRES_PASSWORD=your-secure-password-here
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```

**Important Notes:**
- The [`.env`](.env) file is gitignored and should NEVER be committed to version control
- [`.env.example`](.env.example) contains neutral placeholder values and is safe to commit
- Generate a unique `SECRET_KEY` for production environments
- Use strong passwords for database credentials

## Step 1: Start the PostgreSQL Database

The project includes a [`docker-compose-dev.yaml`](docker-compose-dev.yaml) file that defines a PostgreSQL 17 database with a persistent volume.

Start the database:

```bash
docker-compose -f docker-compose-dev.yaml up -d
```

This command will:
- Download the PostgreSQL 17 Alpine image (first time only)
- Create a Docker container named `diri-planner-postgres`
- Set up a persistent volume named `postgres_data` to store database data
- Expose PostgreSQL on port 5432
- Create a database named `diri_planner` with user `diri_user` and password `diri_password`

Verify the database is running:

```bash
docker-compose -f docker-compose-dev.yaml ps
```

Check database logs:

```bash
docker-compose -f docker-compose-dev.yaml logs db
```

## Step 2: Install Python Dependencies

The project now requires `psycopg2-binary` (PostgreSQL adapter) and `python-dotenv` (environment variable management). Install dependencies using UV:

```bash
uv sync
```

Or if you're using pip:

```bash
pip install -e .
```

## Step 3: Verify Environment Configuration

The Django project loads configuration from your [`.env`](.env) file via [`config/settings.py`](config/settings.py:15). Make sure your [`.env`](.env) file has the correct database credentials matching those in [`docker-compose-dev.yaml`](docker-compose-dev.yaml).

**Default Configuration:**
- **Database**: `diri_planner`
- **User**: `diri_user`
- **Password**: (set in your `.env` file)
- **Host**: `localhost`
- **Port**: `5432`

The application will automatically load these settings from your [`.env`](.env) file when it starts.

## Step 4: Run Django Migrations

Initialize the database schema:

```bash
python manage.py migrate
```

This will create all necessary Django tables in the PostgreSQL database.

## Step 5: Create a Superuser (Optional)

Create an admin user for the Django admin interface:

```bash
python manage.py createsuperuser
```

## Step 6: Run the Development Server

Start the Django development server:

```bash
python manage.py runserver
```

The application will now use PostgreSQL instead of SQLite.

## Managing the Database

### Stop the database

```bash
docker-compose -f docker-compose-dev.yaml stop
```

### Start the database (after stopping)

```bash
docker-compose -f docker-compose-dev.yaml start
```

### Restart the database

```bash
docker-compose -f docker-compose-dev.yaml restart
```

### Stop and remove the database container

```bash
docker-compose -f docker-compose-dev.yaml down
```

**Note**: This removes the container but keeps the data in the `postgres_data` volume.

### Remove database and data volume

```bash
docker-compose -f docker-compose-dev.yaml down -v
```

**Warning**: This will permanently delete all database data!

## Docker Compose Configuration

The [`docker-compose-dev.yaml`](docker-compose-dev.yaml) file includes:

- **PostgreSQL 17 Alpine**: Lightweight PostgreSQL image
- **Persistent Volume**: Data stored in `postgres_data` volume survives container restarts
- **Health Check**: Automatically verifies database is ready
- **Port Mapping**: PostgreSQL accessible on host port 5432
- **Auto-restart**: Container restarts automatically unless stopped manually

## Database Credentials

### Default Credentials

- **Database Name**: `diri_planner`
- **Username**: `diri_user`
- **Password**: `diri_password`
- **Host**: `localhost`
- **Port**: `5432`

### Changing Credentials

To change database credentials, update both files:

1. In [`docker-compose-dev.yaml`](docker-compose-dev.yaml):
   ```yaml
   environment:
     POSTGRES_DB: your_database_name
     POSTGRES_USER: your_username
     POSTGRES_PASSWORD: your_password
   ```

2. In your [`.env`](.env) file:
   ```bash
   POSTGRES_DB=your_database_name
   POSTGRES_USER=your_username
   POSTGRES_PASSWORD=your_password
   ```

**Note:** Never modify [`config/settings.py`](config/settings.py:75) directly for credentials. Always use the [`.env`](.env) file.

## Connecting with Database Tools

You can connect to the database using tools like pgAdmin, DBeaver, or psql:

```bash
psql -h localhost -p 5432 -U diri_user -d diri_planner
```

When prompted, enter the password: `diri_password`

## Troubleshooting

### Database connection refused

- Ensure Docker is running
- Verify the database container is up: `docker-compose -f docker-compose-dev.yaml ps`
- Check if port 5432 is available: `lsof -i :5432` (macOS/Linux) or `netstat -an | findstr 5432` (Windows)

### Port already in use

If you have PostgreSQL already running locally on port 5432, either:

1. Stop the local PostgreSQL service
2. Or change the port mapping in [`docker-compose-dev.yaml`](docker-compose-dev.yaml):
   ```yaml
   ports:
     - "5433:5432"  # Use port 5433 on host instead
   ```
   Then update `POSTGRES_PORT` in your environment variables.

### Permission denied errors

Ensure you have proper permissions to run Docker commands. You may need to add your user to the docker group:

```bash
sudo usermod -aG docker $USER
```

Then log out and log back in.

### Database data persistence

Data is stored in a Docker volume named `postgres_data`. To verify:

```bash
docker volume ls
```

To inspect the volume:

```bash
docker volume inspect diri-planner-15_postgres_data
```

## Migration from SQLite

If you have existing data in SQLite that you want to migrate:

1. Start with the old SQLite database
2. Export your data using Django's `dumpdata`:
   ```bash
   python manage.py dumpdata > data_backup.json
   ```
3. Switch to PostgreSQL (follow steps above)
4. Run migrations: `python manage.py migrate`
5. Import your data:
   ```bash
   python manage.py loaddata data_backup.json
   ```

## Environment Variables Reference

All configuration is managed through the [`.env`](.env) file:

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `SECRET_KEY` | Django secret key | Auto-generated insecure key | Yes (prod) |
| `DEBUG` | Enable debug mode | True | No |
| `POSTGRES_DB` | Database name | diri_planner | Yes |
| `POSTGRES_USER` | Database username | diri_user | Yes |
| `POSTGRES_PASSWORD` | Database password | (none) | Yes |
| `POSTGRES_HOST` | Database host | localhost | Yes |
| `POSTGRES_PORT` | Database port | 5432 | Yes |

## Production Considerations

For production use:

1. **Never commit the `.env` file**: It contains sensitive credentials
2. **Generate a unique SECRET_KEY**: Use Django's `get_random_secret_key()` or an online generator
3. **Use strong passwords**: Generate secure random passwords for database
4. **Set DEBUG=False**: Never run with DEBUG=True in production
5. **Use environment-specific .env files**: Consider `.env.production`, `.env.staging`, etc.
6. **Secret management**: Use proper secret management services (AWS Secrets Manager, HashiCorp Vault, etc.)
7. **Network isolation**: Consider using Docker networks instead of host ports
8. **Backups**: Implement regular database backups
9. **SSL/TLS**: Enable encrypted connections
10. **Resource limits**: Configure appropriate memory and CPU limits in docker-compose

## Summary

The setup provides:
- ✅ PostgreSQL 17 database in Docker
- ✅ Persistent data storage
- ✅ Health checks for reliability
- ✅ Easy management with docker-compose
- ✅ Django configured to use PostgreSQL
- ✅ Environment-based configuration for flexibility