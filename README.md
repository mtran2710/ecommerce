# Django E-commerce Application

This is a full-featured Django e-commerce application with Docker support, PostgreSQL database, and SQLite for development.

## Features

- Product catalog with categories
- Product detail pages
- Docker containerization for easy development
- PostgreSQL database support
- Responsive design with Bootstrap 4

## Requirements

- Python 3.8+
- Django 3.2+
- Docker and Docker Compose (for containerized development)

## Local Development Setup

### 1. Clone the repository

```bash
git clone <repository-url>
cd ecommerce
```

### 2. Create a virtual environment and activate it

```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables
Create a `.env` file in the project root with the following variables:

```
DEBUG=True
DJANGO_SECRET_KEY=django-insecure-rsg4@0%65zug4x__lmb_7yvt+-=pibn80ew7ef2onan8rqv39+
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1,web
DJANGO_CSRF_TRUSTED_ORIGINS=http://localhost:8000

# Database settings
DATABASE_ENGINE=postgresql
DATABASE_NAME=ecommerce_db
DATABASE_USERNAME=dbuser
DATABASE_PASSWORD=dbpassword
DATABASE_HOST=db
DATABASE_PORT=5432

# AWS S3 settings
AWS_ACCESS_KEY_ID=your-access-key-id
AWS_SECRET_ACCESS_KEY=your-secret-access-key

# Default superuser (optional)
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=admin@example.com
DJANGO_SUPERUSER_PASSWORD=admin123
```

### 5. Run migrations

```bash
python manage.py migrate
```

### 6. Create a superuser
You can create a superuser manually or use the provided environment variables:

```bash
python manage.py createsuperuser
# Or use the custom command if implemented:
# python manage.py create_superuser
```

### 7. Collect static files

```bash
python manage.py collectstatic --noinput
```

### 8. Run the development server

```bash
python manage.py runserver
```

The application should now be running at `http://127.0.0.1:8000/`

## Importing Data from SQL Backup (backup.sql)

#### For SQLite (Development)

```bash
# Make sure the database is properly set up first
python manage.py migrate

# Import the SQL data
sqlite3 db.sqlite3 < backup.sql
```

#### For PostgreSQL (Local Development with PostgreSQL)

```bash
# If using PostgreSQL locally
psql -U dbuser -d ecommerce_db -f backup.sql
```

### Docker Environment

For importing data in the Docker environment:

```bash
# Copy the backup file to the database container
docker cp backup.sql ecommerce_db_1:/tmp/backup.sql

# Import the data
docker-compose exec db psql -U dbuser -d ecommerce_db -f /tmp/backup.sql
```

You can verify the data import by checking the tables in the admin interface or by querying the database:

```bash
# For local development
python manage.py dbshell

# For Docker
docker-compose exec db psql -U dbuser -d ecommerce_db
```

## Docker Development

The project includes an entrypoint.sh script that automatically handles:
- Waiting for the database to be ready
- Running migrations
- Collecting static files
- Creating a superuser if it doesn't exist
- Starting the development server

### Build and run with Docker Compose

```bash
docker-compose up -d --build
```

The application should now be running at `http://localhost:8000/`

## Troubleshooting

### Static Files Not Loading

1. Check if `DEBUG=True` in development
2. Ensure `STATIC_URL` and `STATIC_ROOT` are correctly configured

### Database Connection Issues

1. Check database credentials in `.env`
2. For Docker: ensure the database service is running:

```bash
docker-compose ps
```

3. Wait a few moments after starting containers to allow the database to initialize

### Missing psycopg2 Module

Install the required package:

```bash
# For local development
pip install psycopg2-binary

# For Docker, ensure it's in requirements.txt
```

## Project Structure

- `core/`: Core application with models, views, and URLs
- `ecommerce/`: Project settings and configuration
- `media/`: Local media files
- `static/`: Static files (CSS, JS, images)
- `templates/`: HTML templates
- `docker-compose.yml`: Docker services configuration
- `Dockerfile`: Docker container configuration
- `entrypoint.sh`: Docker container startup script
- `.env`: Development environment variables
- `backup.sql`: Database backup file